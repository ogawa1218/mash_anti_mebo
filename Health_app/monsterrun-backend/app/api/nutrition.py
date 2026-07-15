"""栄養ログの登録と、栄養エンジンによる日次評価。"""

import uuid
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import current_user_id
from app.db import get_session
from app.engine.nutrition import (
    NutritionInput,
    bmr_mifflin_st_jeor,
    condition_to_animation,
    evaluate,
)
from app.models import (
    ActivityStatus,
    DailyConditionSnapshot,
    Monster,
    MonsterEffect,
    NutritionLog,
    User,
    WearableActivity,
)
from app.schemas.nutrition import ConditionResult, NutritionLogIn

router = APIRouter(prefix="/v1/nutrition", tags=["nutrition"])


@router.post("/logs", response_model=ConditionResult)
async def upsert_nutrition_log(
    body: NutritionLogIn,
    user_id: uuid.UUID = Depends(current_user_id),
    session: AsyncSession = Depends(get_session),
) -> ConditionResult:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    totals = body.totals
    stmt = pg_insert(NutritionLog).values(
        user_id=user_id, log_date=body.log_date, source=body.source,
        meals=[m.model_dump(mode="json") for m in body.meals], **totals,
    ).on_conflict_do_update(
        index_elements=["user_id", "log_date", "source"],
        set_={**totals, "meals": [m.model_dump(mode="json") for m in body.meals],
              "updated_at": func.now()},
    )
    await session.execute(stmt)

    result = await _evaluate_day(session, user, body.log_date)
    await _apply_effects(session, user_id, result)
    return result


async def _evaluate_day(session: AsyncSession, user: User, day: date) -> ConditionResult:
    active_kcal = await session.scalar(
        select(func.coalesce(func.sum(WearableActivity.calories_active), 0)).where(
            WearableActivity.user_id == user.id,
            WearableActivity.status.in_([ActivityStatus.accepted, ActivityStatus.flagged]),
            func.date(WearableActivity.started_at) == day,
        )
    )
    totals = (await session.execute(
        select(
            func.coalesce(func.sum(NutritionLog.calories_in), 0),
            func.coalesce(func.sum(NutritionLog.protein_g), 0),
            func.coalesce(func.sum(NutritionLog.fat_g), 0),
            func.coalesce(func.sum(NutritionLog.carbs_g), 0),
        ).where(NutritionLog.user_id == user.id, NutritionLog.log_date == day)
    )).one()

    age = (day - user.date_of_birth).days // 365 if user.date_of_birth else 40
    bmr = bmr_mifflin_st_jeor(
        float(user.weight_kg or 70), float(user.height_cm or 170), age, user.sex or "male"
    )
    result = evaluate(NutritionInput(
        calories_in=float(totals[0]), protein_g=float(totals[1]),
        fat_g=float(totals[2]), carbs_g=float(totals[3]),
        active_calories=float(active_kcal), bmr_kcal=bmr,
        weight_kg=float(user.weight_kg or 70),
    ))

    snap = pg_insert(DailyConditionSnapshot).values(
        user_id=user.id, snapshot_date=day,
        energy_balance_kcal=result.energy_balance_kcal,
        pfc_score=result.pfc_score, condition_score=result.condition_score,
        effects_applied=result.effects,
    ).on_conflict_do_update(
        index_elements=["user_id", "snapshot_date"],
        set_={"energy_balance_kcal": result.energy_balance_kcal,
              "pfc_score": result.pfc_score, "condition_score": result.condition_score,
              "effects_applied": result.effects},
    )
    await session.execute(snap)
    return result


async def _apply_effects(session: AsyncSession, user_id: uuid.UUID, result: ConditionResult) -> None:
    monster = await session.scalar(select(Monster).where(Monster.user_id == user_id, Monster.is_active))
    if monster is None:
        return
    # 当日分の nutrition_engine 効果は洗い替え
    now = datetime.now(timezone.utc)
    existing = await session.execute(
        select(MonsterEffect).where(
            MonsterEffect.monster_id == monster.id,
            MonsterEffect.granted_by == "nutrition_engine",
            MonsterEffect.expires_at > now,
        )
    )
    for e in existing.scalars():
        await session.delete(e)
    for eff in result.effects:
        session.add(MonsterEffect(
            monster_id=monster.id, kind=eff["kind"], code=eff["code"],
            exp_multiplier=eff["exp_multiplier"], granted_by="nutrition_engine",
            expires_at=now + timedelta(hours=24),
        ))
    monster.condition_score = result.condition_score
    monster.animation_state = condition_to_animation(result.condition_score)
