"""インジェストワーカー。

Redis Streams `ingest:activities` を consumer group で購読し、1件ずつ:
  1. Normalizer で NormalizedActivity へ変換
  2. provider_user_id → 内部ユーザー解決
  3. 冪等チェック（source+external_id）と時間窓オーバーラップ重複排除
  4. Anti-Cheat 評価
  5. accepted/flagged なら Growth + Evolution を計算し exp_ledger に記帳
  6. monsters を更新、Redisキャッシュ無効化・リーダーボード更新

起動: python -m app.ingestion.pipeline
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import SessionLocal, redis_client
from app.engine.anticheat import AntiCheatEngine
from app.engine.evolution import (
    EVOLUTION_TABLE,
    decide_branch,
    evolution_points,
    gauge_increment,
    zone_seconds_from_avg,
    zone_seconds_from_samples,
    GAUGE_FULL,
)
from app.engine.growth import ExpInput, apply_exp_to_level, calc_exp
from app.engine.nutrition import combined_multiplier
from app.ingestion.apple_healthkit import AppleHealthKitNormalizer
from app.ingestion.base import ActivityNormalizer
from app.ingestion.garmin import GarminNormalizer
from app.ingestion.google_health_connect import GoogleHealthConnectNormalizer
from app.ingestion.strava import StravaNormalizer
from app.models import (
    ActivityStatus,
    EvolutionHistory,
    ExpLedger,
    Monster,
    MonsterEffect,
    User,
    WearableActivity,
    WearableConnection,
    WearableSource,
)
from app.schemas.activity import NormalizedActivity
from app.security.oauth import get_valid_access_token

logger = logging.getLogger("ingest")
settings = get_settings()

NORMALIZERS: dict[str, ActivityNormalizer] = {
    "garmin": GarminNormalizer(),
    "strava": StravaNormalizer(),
    "apple_healthkit": AppleHealthKitNormalizer(),
    "google_health_connect": GoogleHealthConnectNormalizer(),
}

anticheat = AntiCheatEngine()


async def enqueue(source: str, payload: dict) -> str:
    """API層から呼ぶ: 生ペイロードをキューへ（Webhookは即200を返すため処理を分離）。"""
    return await redis_client.xadd(
        settings.ingest_stream,
        {"source": source, "payload": json.dumps(payload, default=str)},
        maxlen=100_000,
        approximate=True,
    )


async def _resolve_user(session: AsyncSession, act: NormalizedActivity) -> User | None:
    if act.source in ("apple_healthkit", "google_health_connect", "manual"):
        return await session.get(User, act.provider_user_id)  # JWT由来の内部ID
    row = await session.execute(
        select(WearableConnection)
        .where(
            WearableConnection.source == WearableSource(act.source),
            WearableConnection.provider_user_id == act.provider_user_id,
            WearableConnection.is_active,
        )
    )
    conn = row.scalar_one_or_none()
    return await session.get(User, conn.user_id) if conn else None


async def _is_cross_source_duplicate(session: AsyncSession, user: User, act: NormalizedActivity) -> bool:
    """別ソースで時間窓が50%以上重複する受理済み活動があれば duplicate。
    （例: Garminで記録したランがStravaにも自動同期されるケース）"""
    overlap_q = select(WearableActivity).where(
        WearableActivity.user_id == user.id,
        WearableActivity.source != WearableSource(act.source),
        WearableActivity.status.in_([ActivityStatus.accepted, ActivityStatus.flagged]),
        WearableActivity.started_at < act.ended_at,
        WearableActivity.ended_at > act.started_at,
    )
    for existing in (await session.execute(overlap_q)).scalars():
        overlap_s = (
            min(existing.ended_at, act.ended_at) - max(existing.started_at, act.started_at)
        ).total_seconds()
        if overlap_s >= 0.5 * min(existing.duration_s, act.duration_s):
            return True
    return False


async def _active_effect_multiplier(session: AsyncSession, monster: Monster) -> float:
    now = datetime.now(timezone.utc)
    rows = await session.execute(
        select(MonsterEffect).where(
            MonsterEffect.monster_id == monster.id, MonsterEffect.expires_at > now
        )
    )
    return combined_multiplier([{"exp_multiplier": e.exp_multiplier} for e in rows.scalars()])


async def _lifetime_distance_km(session: AsyncSession, user_id) -> float:
    total = await session.scalar(
        select(func.coalesce(func.sum(WearableActivity.distance_m), 0)).where(
            WearableActivity.user_id == user_id,
            WearableActivity.status.in_([ActivityStatus.accepted, ActivityStatus.flagged]),
        )
    )
    return float(total) / 1000.0


async def process_activity(session: AsyncSession, act: NormalizedActivity) -> WearableActivity | None:
    """正規化済み活動1件を判定・記帳・反映する（トランザクション内で呼ぶ）。"""
    user = await _resolve_user(session, act)
    if user is None:
        logger.warning("no user for %s/%s", act.source, act.provider_user_id)
        return None

    # 冪等: 同一 (source, external_id) は skip
    dup = await session.scalar(
        select(WearableActivity.id).where(
            WearableActivity.source == WearableSource(act.source),
            WearableActivity.external_id == act.external_id,
        )
    )
    if dup:
        return None

    verdict = anticheat.evaluate(act, hr_rest=user.hr_rest)
    status = ActivityStatus(verdict.status)
    if await _is_cross_source_duplicate(session, user, act):
        status = ActivityStatus.duplicate

    hr_max = user.estimated_hr_max()
    if act.hr_samples:
        zones = zone_seconds_from_samples(act.hr_samples, user.hr_rest, hr_max)
    elif act.hr_avg:
        zones = zone_seconds_from_avg(act.hr_avg, act.duration_s, user.hr_rest, hr_max)
    else:
        zones = None

    row = WearableActivity(
        user_id=user.id,
        source=WearableSource(act.source),
        external_id=act.external_id,
        activity_type=act.activity_type,
        started_at=act.started_at,
        ended_at=act.ended_at,
        duration_s=act.duration_s,
        distance_m=act.distance_m,
        steps=act.steps,
        calories_active=act.calories_active,
        hr_avg=act.hr_avg,
        hr_max=act.hr_max,
        hr_samples=[s.model_dump() for s in act.hr_samples] or None,
        gps_samples=[s.model_dump() for s in act.gps_samples] or None,
        elevation_gain_m=act.elevation_gain_m,
        temperature_c=act.temperature_c,
        status=status,
        cheat_score=verdict.score,
        cheat_flags=verdict.as_json(),
        zone_seconds=zones,
    )
    session.add(row)
    await session.flush()

    if status in (ActivityStatus.accepted, ActivityStatus.flagged):
        await _award(session, user, row, zones)
    return row


async def _award(session: AsyncSession, user: User, row: WearableActivity, zones: dict | None) -> None:
    monster = await session.scalar(
        select(Monster).where(Monster.user_id == user.id, Monster.is_active).with_for_update()
    )
    if monster is None:
        return

    result = calc_exp(ExpInput(
        distance_km=float(row.distance_m) / 1000.0,
        hr_avg=row.hr_avg,
        hr_rest=user.hr_rest,
        temperature_c=float(row.temperature_c) if row.temperature_c is not None else None,
        lifetime_distance_km=await _lifetime_distance_km(session, user.id),
        alpha=settings.exp_alpha,
        effect_multiplier=await _active_effect_multiplier(session, monster),
    ))
    delta = evolution_points(zones or {})

    session.add(ExpLedger(
        monster_id=monster.id,
        activity_id=row.id,
        idempotency_key=f"activity:{row.id}",
        exp_delta=result.exp,
        stamina_delta=delta.stamina_points,
        speed_delta=delta.speed_points,
        reason="activity",
        metadata_=result.breakdown,
    ))
    row.exp_awarded = result.exp

    monster.level, monster.exp = apply_exp_to_level(monster.level, float(monster.exp), result.exp)
    monster.stamina_points = float(monster.stamina_points) + delta.stamina_points
    monster.speed_points = float(monster.speed_points) + delta.speed_points
    monster.evolution_gauge = min(float(monster.evolution_gauge) + gauge_increment(delta), GAUGE_FULL)
    monster.animation_state = "training"

    if float(monster.evolution_gauge) >= GAUGE_FULL:
        _evolve(session, monster)

    # キャッシュ無効化 + 週間リーダーボード
    await redis_client.delete(f"user:{user.id}:monster")
    await redis_client.zincrby("leaderboard:weekly_exp", result.exp, str(user.id))


def _evolve(session: AsyncSession, monster: Monster) -> None:
    line = decide_branch(float(monster.stamina_points), float(monster.speed_points))
    spec = EVOLUTION_TABLE[line]
    old_species = monster.species_code
    monster.species_code = f"runmon_g{monster.generation + 1}_{spec['species_suffix']}"
    monster.generation += 1
    monster.evolution_line = line
    monster.evolution_gauge = 0
    for stat, mult in spec["stat_bonus"].items():
        setattr(monster, stat, round(float(getattr(monster, stat)) * mult, 2))
    monster.animation_state = "evolving"
    session.add(EvolutionHistory(
        monster_id=monster.id,
        from_species=old_species,
        to_species=monster.species_code,
        line=line,
        stamina_points=monster.stamina_points,
        speed_points=monster.speed_points,
    ))


# ---------------------------------------------------------------------------
# ワーカーループ
# ---------------------------------------------------------------------------
async def _handle_message(fields: dict) -> None:
    source = fields["source"]
    payload = json.loads(fields["payload"])
    normalizer = NORMALIZERS[source]

    async with SessionLocal() as session:
        async with session.begin():
            if source == "strava":
                # fetch-on-event: トークンを解決してからAPI取得
                conn = await session.scalar(
                    select(WearableConnection).where(
                        WearableConnection.source == WearableSource.strava,
                        WearableConnection.provider_user_id == str(payload.get("owner_id")),
                        WearableConnection.is_active,
                    )
                )
                if conn is None:
                    return
                token = await get_valid_access_token(session, conn)
                activities = await normalizer.fetch_and_normalize(payload, token)  # type: ignore[attr-defined]
            else:
                activities = normalizer.normalize(payload)

            for act in activities:
                await process_activity(session, act)


async def run_worker(consumer_name: str = "worker-1") -> None:
    try:
        await redis_client.xgroup_create(settings.ingest_stream, settings.ingest_group, mkstream=True)
    except Exception:
        pass  # group already exists

    logger.info("ingest worker started: %s", consumer_name)
    while True:
        messages = await redis_client.xreadgroup(
            settings.ingest_group, consumer_name,
            {settings.ingest_stream: ">"}, count=10, block=5000,
        )
        for _stream, entries in messages or []:
            for msg_id, fields in entries:
                try:
                    await _handle_message(fields)
                    await redis_client.xack(settings.ingest_stream, settings.ingest_group, msg_id)
                except Exception:
                    logger.exception("failed to process %s (left pending for retry)", msg_id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_worker())
