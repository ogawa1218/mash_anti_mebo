"""Async SQLAlchemy engine/session and Redis client factories."""

from collections.abc import AsyncIterator

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

redis_client: aioredis.Redis = aioredis.from_url(settings.redis_url, decode_responses=True)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one transaction per request."""
    async with SessionLocal() as session:
        async with session.begin():
            yield session


async def get_redis() -> aioredis.Redis:
    return redis_client
