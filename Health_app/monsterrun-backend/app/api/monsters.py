"""モンスターステータス参照API（フロントエンドWebGL用）。Redisキャッシュ付き。"""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import current_user_id
from app.db import get_session, redis_client
from app.engine.growth import exp_required_for_level
from app.models import Monster

router = APIRouter(prefix="/v1/monsters", tags=["monsters"])

CACHE_TTL_S = 300


def _serialize(m: Monster) -> dict:
    return {
        "id": str(m.id),
        "name": m.name,
        "species_code": m.species_code,
        "generation": m.generation,
        "level": m.level,
        "exp": float(m.exp),
        "exp_to_next_level": exp_required_for_level(m.level),
        "stats": {
            "stamina": float(m.stamina), "agility": float(m.agility),
            "attack": float(m.attack), "defense": float(m.defense),
            "heart_points": float(m.heart_points),
        },
        "evolution": {
            "line": m.evolution_line.value,
            "gauge": float(m.evolution_gauge),
            "stamina_points": float(m.stamina_points),
            "speed_points": float(m.speed_points),
        },
        "condition_score": m.condition_score,
        "animation_state": m.animation_state.value,
    }


@router.get("/me")
async def get_my_monster(
    user_id: uuid.UUID = Depends(current_user_id),
    session: AsyncSession = Depends(get_session),
) -> dict:
    cache_key = f"user:{user_id}:monster"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    monster = await session.scalar(select(Monster).where(Monster.user_id == user_id, Monster.is_active))
    if monster is None:
        raise HTTPException(status_code=404, detail="no active monster")

    data = _serialize(monster)
    await redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL_S)
    return data
