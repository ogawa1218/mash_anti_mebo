"""Application settings loaded from environment (.env)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://monsterrun:monsterrun@localhost:5432/monsterrun"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "dev-secret"
    token_encryption_key: str = ""

    garmin_client_id: str = ""
    garmin_client_secret: str = ""
    strava_client_id: str = ""
    strava_client_secret: str = ""
    strava_verify_token: str = "monsterrun-strava-verify"

    mcp_service_token: str = "change-me"
    mcp_max_exp_per_call: float = 500.0

    # Game tuning
    exp_alpha: float = 10.0
    ingest_stream: str = "ingest:activities"
    ingest_group: str = "workers"


@lru_cache
def get_settings() -> Settings:
    return Settings()
