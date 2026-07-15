"""OAuthトークンの暗号化保管とリフレッシュ。

- DBには Fernet(AES-128-CBC + HMAC-SHA256) 暗号文のみ保存
- 復号はプロセスメモリ内のみ。ログ・例外メッセージへ平文を出さない
"""

from datetime import datetime, timedelta, timezone

import httpx
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import WearableConnection

settings = get_settings()
_fernet = Fernet(settings.token_encryption_key.encode()) if settings.token_encryption_key else None


def encrypt_token(plain: str) -> str:
    if _fernet is None:
        raise RuntimeError("TOKEN_ENCRYPTION_KEY is not configured")
    return _fernet.encrypt(plain.encode()).decode()


def decrypt_token(cipher: str) -> str:
    if _fernet is None:
        raise RuntimeError("TOKEN_ENCRYPTION_KEY is not configured")
    return _fernet.decrypt(cipher.encode()).decode()


async def get_valid_access_token(session: AsyncSession, conn: WearableConnection) -> str:
    """有効なアクセストークンを返す。期限切れ間近ならリフレッシュしてDB更新。"""
    now = datetime.now(timezone.utc)
    if conn.token_expires_at and conn.token_expires_at > now + timedelta(minutes=5):
        return decrypt_token(conn.access_token_enc)
    if not conn.refresh_token_enc:
        return decrypt_token(conn.access_token_enc)

    refreshed = await _refresh(conn.source.value, decrypt_token(conn.refresh_token_enc))
    conn.access_token_enc = encrypt_token(refreshed["access_token"])
    if refreshed.get("refresh_token"):
        conn.refresh_token_enc = encrypt_token(refreshed["refresh_token"])
    if refreshed.get("expires_at"):
        conn.token_expires_at = datetime.fromtimestamp(refreshed["expires_at"], tz=timezone.utc)
    await session.flush()
    return refreshed["access_token"]


async def _refresh(source: str, refresh_token: str) -> dict:
    if source == "strava":
        url, data = "https://www.strava.com/oauth/token", {
            "client_id": settings.strava_client_id,
            "client_secret": settings.strava_client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    elif source == "garmin":
        url, data = "https://diauth.garmin.com/di-oauth2-service/oauth/token", {
            "client_id": settings.garmin_client_id,
            "client_secret": settings.garmin_client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    else:
        raise ValueError(f"unsupported refresh source: {source}")

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(url, data=data)
        resp.raise_for_status()
        body = resp.json()
    if "expires_at" not in body and "expires_in" in body:
        body["expires_at"] = int(datetime.now(timezone.utc).timestamp()) + int(body["expires_in"])
    return body
