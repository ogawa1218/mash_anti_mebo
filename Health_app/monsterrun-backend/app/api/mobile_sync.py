"""HealthKit / Health Connect のモバイル同期エンドポイント。"""

import uuid

from fastapi import APIRouter, Depends

from app.api.auth import current_user_id
from app.db import SessionLocal
from app.ingestion.pipeline import enqueue
from app.models import RawPayload, WearableSource
from app.schemas.activity import MobileSyncRequest

router = APIRouter(prefix="/v1/sync", tags=["mobile"])


@router.post("/mobile", status_code=202)
async def sync_mobile(
    body: MobileSyncRequest,
    user_id: uuid.UUID = Depends(current_user_id),
) -> dict:
    payload = body.model_dump(mode="json")
    payload["user_id"] = str(user_id)  # 正規化時の provider_user_id はJWT由来の内部IDを使用

    async with SessionLocal() as session:
        async with session.begin():
            session.add(RawPayload(source=WearableSource(body.platform), payload=payload))
    await enqueue(body.platform, payload)

    count = len(body.healthkit_workouts) + len(body.health_connect_sessions)
    return {"queued": count, "status": "accepted"}
