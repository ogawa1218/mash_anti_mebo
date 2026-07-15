"""Project MonsterRun — FastAPI エントリポイント。

起動: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import mobile_sync, monsters, nutrition, webhooks_garmin, webhooks_strava
from app.db import engine, redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()
    await engine.dispose()


app = FastAPI(
    title="Project MonsterRun API",
    version="0.1.0",
    description="ウェアラブル連動デジタル生命体育成ゲームのバックエンド",
    lifespan=lifespan,
)

app.include_router(webhooks_garmin.router)
app.include_router(webhooks_strava.router)
app.include_router(mobile_sync.router)
app.include_router(nutrition.router)
app.include_router(monsters.router)


@app.get("/healthz", tags=["ops"])
async def healthz() -> dict:
    return {"status": "ok"}
