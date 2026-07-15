"""Garmin Push Webhook 受信。

Garminは登録エンドポイントへ activityDetails 等をPOSTする。
3秒以内に応答しないと再送→最終的に配信停止されるため、
検証と raw_payloads 保存のみ行い即 200 を返す（処理はワーカーへ）。
"""

import logging

from fastapi import APIRouter, Request, Response

from app.db import SessionLocal, redis_client
from app.ingestion.pipeline import enqueue
from app.models import RawPayload, WearableSource

router = APIRouter(prefix="/webhooks/garmin", tags=["webhooks"])
logger = logging.getLogger("webhook.garmin")

RATE_LIMIT_PER_MIN = 600


@router.post("/activities", status_code=200)
async def receive_garmin_activities(request: Request) -> Response:
    key = "ratelimit:webhook:garmin:global"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, 60)
    if count > RATE_LIMIT_PER_MIN:
        return Response(status_code=429)

    try:
        payload = await request.json()
    except Exception:
        return Response(status_code=200)  # 不正ペイロードでも200（Garminの再送ループ防止）

    async with SessionLocal() as session:
        async with session.begin():
            session.add(RawPayload(source=WearableSource.garmin, payload=payload))
    await enqueue("garmin", payload)
    return Response(status_code=200)
