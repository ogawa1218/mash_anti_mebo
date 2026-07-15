"""Strava Webhook Subscription 受信。

- GET  : サブスクリプション作成時の hub.challenge エコーバック検証
- POST : イベント受信（中身は含まれないため owner_id と object_id をキューへ）
"""

import logging

from fastapi import APIRouter, HTTPException, Query, Request, Response

from app.config import get_settings
from app.db import SessionLocal
from app.ingestion.pipeline import enqueue
from app.models import RawPayload, WearableSource

router = APIRouter(prefix="/webhooks/strava", tags=["webhooks"])
logger = logging.getLogger("webhook.strava")
settings = get_settings()


@router.get("")
async def verify_subscription(
    hub_mode: str = Query(alias="hub.mode"),
    hub_challenge: str = Query(alias="hub.challenge"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
) -> dict:
    if hub_mode != "subscribe" or hub_verify_token != settings.strava_verify_token:
        raise HTTPException(status_code=403, detail="verify token mismatch")
    return {"hub.challenge": hub_challenge}


@router.post("", status_code=200)
async def receive_strava_event(request: Request) -> Response:
    payload = await request.json()
    async with SessionLocal() as session:
        async with session.begin():
            session.add(RawPayload(
                source=WearableSource.strava,
                external_id=str(payload.get("object_id", "")),
                payload=payload,
            ))
    await enqueue("strava", payload)
    return Response(status_code=200)
