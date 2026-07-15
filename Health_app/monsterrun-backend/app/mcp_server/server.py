"""MonsterRun MCP Server — JSON-RPC 2.0 (Model Context Protocol)。

LLM（Claude / Gemini 等）がユーザー・モンスター情報を安全に読み書きし、
パーソナライズされたコーチングを行うためのツール群を公開する。

トランスポート:
  - stdio             : python -m app.mcp_server.server
  - Streamable HTTP   : app.main に /mcp としてマウント可能（Bearer認証）

セキュリティ設計:
  - 読取ツールは read:status、書込は write:exp スコープ
  - 書込は idempotency_key 必須（Redisで24h記憶、再送は前回結果を返す）
  - EXPはサーバー側で MCP_MAX_EXP_PER_CALL にクランプ → LLMの幻覚による無限付与を構造的に防止
  - バフは code ホワイトリスト制
  - 応答にPII（メール・氏名）を含めない
"""

import asyncio
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.config import get_settings
from app.db import SessionLocal, redis_client
from app.engine.growth import apply_exp_to_level, exp_required_for_level
from app.models import (
    ActivityStatus,
    DailyConditionSnapshot,
    ExpLedger,
    Monster,
    MonsterEffect,
    NutritionLog,
    User,
    WearableActivity,
)

settings = get_settings()

PROTOCOL_VERSION = "2025-06-18"
COACHING_BUFF_WHITELIST = {
    "well_rested": 1.05,
    "hydration_hero": 1.05,
    "consistency_streak": 1.10,
    "sleep_champion": 1.08,
}

with open("mcp/tools.json", encoding="utf-8") as f:
    TOOLS_MANIFEST = json.load(f)


# ---------------------------------------------------------------------------
# ツール実装
# ---------------------------------------------------------------------------
async def tool_get_user_status(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        if user is None:
            raise ToolError("user not found")

        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        rows = (await session.execute(
            select(WearableActivity).where(
                WearableActivity.user_id == user_id,
                WearableActivity.started_at >= week_ago,
                WearableActivity.status.in_([ActivityStatus.accepted, ActivityStatus.flagged]),
            )
        )).scalars().all()

        zone_minutes = {f"z{i}": 0.0 for i in range(1, 6)}
        for a in rows:
            for z, s in (a.zone_seconds or {}).items():
                zone_minutes[z] = round(zone_minutes.get(z, 0) + s / 60, 1)

        snap = await session.get(
            DailyConditionSnapshot, {"user_id": user_id, "snapshot_date": datetime.now(timezone.utc).date()}
        )

        return {
            "hr_rest": user.hr_rest,
            "hr_max_estimated": user.estimated_hr_max(),
            "weight_kg": float(user.weight_kg) if user.weight_kg else None,
            "last_7d": {
                "activities": len(rows),
                "distance_km": round(sum(float(a.distance_m) for a in rows) / 1000, 2),
                "exp_gained": round(sum(float(a.exp_awarded or 0) for a in rows), 2),
                "zone_minutes": zone_minutes,
            },
            "today_condition": {
                "condition_score": snap.condition_score,
                "energy_balance_kcal": float(snap.energy_balance_kcal),
                "pfc_score": snap.pfc_score,
            } if snap else None,
        }


async def tool_get_monster_status(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    async with SessionLocal() as session:
        monster = await session.scalar(
            select(Monster).where(Monster.user_id == user_id, Monster.is_active)
        )
        if monster is None:
            raise ToolError("no active monster")
        now = datetime.now(timezone.utc)
        effects = (await session.execute(
            select(MonsterEffect).where(
                MonsterEffect.monster_id == monster.id, MonsterEffect.expires_at > now
            )
        )).scalars().all()
        return {
            "name": monster.name,
            "species_code": monster.species_code,
            "generation": monster.generation,
            "level": monster.level,
            "exp": float(monster.exp),
            "exp_to_next_level": exp_required_for_level(monster.level),
            "stats": {
                "stamina": float(monster.stamina), "agility": float(monster.agility),
                "attack": float(monster.attack), "defense": float(monster.defense),
                "heart_points": float(monster.heart_points),
            },
            "evolution": {
                "line": monster.evolution_line.value,
                "gauge_pct": float(monster.evolution_gauge),
                "stamina_points": float(monster.stamina_points),
                "speed_points": float(monster.speed_points),
            },
            "condition_score": monster.condition_score,
            "animation_state": monster.animation_state.value,
            "active_effects": [
                {"kind": e.kind.value, "code": e.code,
                 "exp_multiplier": float(e.exp_multiplier),
                 "expires_at": e.expires_at.isoformat()}
                for e in effects
            ],
        }


async def tool_get_recent_activities(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    limit = min(int(args.get("limit", 10)), 50)
    async with SessionLocal() as session:
        q = select(WearableActivity).where(WearableActivity.user_id == user_id)
        if args.get("activity_type"):
            q = q.where(WearableActivity.activity_type == args["activity_type"])
        rows = (await session.execute(
            q.order_by(WearableActivity.started_at.desc()).limit(limit)
        )).scalars().all()
        return {"activities": [
            {
                "started_at": a.started_at.isoformat(),
                "type": a.activity_type.value,
                "distance_km": round(float(a.distance_m) / 1000, 2),
                "duration_min": round(a.duration_s / 60, 1),
                "hr_avg": a.hr_avg,
                "exp_awarded": float(a.exp_awarded) if a.exp_awarded else None,
                "status": a.status.value,
            } for a in rows
        ]}


async def tool_get_nutrition_summary(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    days = min(int(args.get("days", 7)), 30)
    since = datetime.now(timezone.utc).date() - timedelta(days=days - 1)
    async with SessionLocal() as session:
        logs = (await session.execute(
            select(NutritionLog).where(
                NutritionLog.user_id == user_id, NutritionLog.log_date >= since
            ).order_by(NutritionLog.log_date.desc())
        )).scalars().all()
        snaps = (await session.execute(
            select(DailyConditionSnapshot).where(
                DailyConditionSnapshot.user_id == user_id,
                DailyConditionSnapshot.snapshot_date >= since,
            )
        )).scalars().all()
        snap_by_date = {s.snapshot_date: s for s in snaps}
        return {"days": [
            {
                "date": log.log_date.isoformat(),
                "calories_in": float(log.calories_in),
                "protein_g": float(log.protein_g),
                "fat_g": float(log.fat_g),
                "carbs_g": float(log.carbs_g),
                "energy_balance_kcal": float(snap_by_date[log.log_date].energy_balance_kcal)
                    if log.log_date in snap_by_date else None,
                "condition_score": snap_by_date[log.log_date].condition_score
                    if log.log_date in snap_by_date else None,
            } for log in logs
        ]}


async def tool_apply_training_exp(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    idem_key = f"mcp:{args['idempotency_key']}"
    exp = min(max(float(args["exp"]), 1.0), settings.mcp_max_exp_per_call)  # サーバー側クランプ

    cached = await redis_client.get(f"mcp:idempotency:{idem_key}")
    if cached:
        return json.loads(cached)

    async with SessionLocal() as session:
        async with session.begin():
            monster = await session.scalar(
                select(Monster).where(Monster.user_id == user_id, Monster.is_active).with_for_update()
            )
            if monster is None:
                raise ToolError("no active monster")
            # DB側の一意制約でも二重付与を防止
            existing = await session.scalar(
                select(ExpLedger).where(ExpLedger.idempotency_key == idem_key)
            )
            if existing:
                result = {"applied": False, "reason": "duplicate idempotency_key",
                          "level": monster.level, "exp": float(monster.exp)}
            else:
                session.add(ExpLedger(
                    monster_id=monster.id, idempotency_key=idem_key,
                    exp_delta=exp, reason="mcp_coaching",
                    metadata_={"tool": "apply_training_exp", "note": args["reason"][:200]},
                ))
                monster.level, monster.exp = apply_exp_to_level(monster.level, float(monster.exp), exp)
                await redis_client.delete(f"user:{user_id}:monster")
                result = {"applied": True, "exp_applied": exp,
                          "level": monster.level, "exp": float(monster.exp)}

    await redis_client.set(f"mcp:idempotency:{idem_key}", json.dumps(result), ex=86400)
    return result


async def tool_grant_coaching_buff(args: dict) -> dict:
    user_id = uuid.UUID(args["user_id"])
    code = args["code"]
    if code not in COACHING_BUFF_WHITELIST:
        raise ToolError(f"buff code '{code}' is not whitelisted")
    hours = min(int(args.get("duration_hours", 24)), 72)
    idem_key = f"mcp:buff:{args['idempotency_key']}"

    cached = await redis_client.get(f"mcp:idempotency:{idem_key}")
    if cached:
        return json.loads(cached)

    async with SessionLocal() as session:
        async with session.begin():
            monster = await session.scalar(
                select(Monster).where(Monster.user_id == user_id, Monster.is_active)
            )
            if monster is None:
                raise ToolError("no active monster")
            expires = datetime.now(timezone.utc) + timedelta(hours=hours)
            session.add(MonsterEffect(
                monster_id=monster.id, kind="buff", code=code,
                exp_multiplier=COACHING_BUFF_WHITELIST[code],
                granted_by="mcp:grant_coaching_buff", expires_at=expires,
            ))
            await redis_client.delete(f"user:{user_id}:monster")
            result = {"granted": True, "code": code,
                      "exp_multiplier": COACHING_BUFF_WHITELIST[code],
                      "expires_at": expires.isoformat()}

    await redis_client.set(f"mcp:idempotency:{idem_key}", json.dumps(result), ex=86400)
    return result


TOOL_HANDLERS = {
    "get_user_status": tool_get_user_status,
    "get_monster_status": tool_get_monster_status,
    "get_recent_activities": tool_get_recent_activities,
    "get_nutrition_summary": tool_get_nutrition_summary,
    "apply_training_exp": tool_apply_training_exp,
    "grant_coaching_buff": tool_grant_coaching_buff,
}


class ToolError(Exception):
    pass


# ---------------------------------------------------------------------------
# JSON-RPC 2.0 ディスパッチ
# ---------------------------------------------------------------------------
async def handle_jsonrpc(request: dict) -> dict | None:
    req_id = request.get("id")
    method = request.get("method")

    def ok(result: dict) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    def err(code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    try:
        if method == "initialize":
            return ok({
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": TOOLS_MANIFEST["serverInfo"],
            })
        if method == "notifications/initialized":
            return None  # notification: 応答不要
        if method == "tools/list":
            return ok({"tools": TOOLS_MANIFEST["tools"]})
        if method == "tools/call":
            params = request.get("params", {})
            name = params.get("name")
            handler = TOOL_HANDLERS.get(name)
            if handler is None:
                return err(-32602, f"unknown tool: {name}")
            try:
                result = await handler(params.get("arguments", {}))
                return ok({"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                           "isError": False})
            except ToolError as e:
                return ok({"content": [{"type": "text", "text": str(e)}], "isError": True})
        if method == "ping":
            return ok({})
        return err(-32601, f"method not found: {method}")
    except Exception as e:  # noqa: BLE001
        return err(-32603, f"internal error: {type(e).__name__}")


async def stdio_main() -> None:
    """stdioトランスポート: 1行1メッセージのJSON-RPC。"""
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)

    while True:
        line = await reader.readline()
        if not line:
            break
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = await handle_jsonrpc(request)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(stdio_main())
