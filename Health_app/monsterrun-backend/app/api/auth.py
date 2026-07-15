"""モバイルアプリJWT認証の共通依存。"""

import uuid

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()
bearer = HTTPBearer()

ALGORITHM = "HS256"


def current_user_id(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> uuid.UUID:
    try:
        claims = jwt.decode(creds.credentials, settings.secret_key, algorithms=[ALGORITHM])
        return uuid.UUID(claims["sub"])
    except (JWTError, KeyError, ValueError) as e:
        raise HTTPException(status_code=401, detail="invalid token") from e
