
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets

import jwt
from fastapi import Response
from pwdlib import PasswordHash

from config.settings import (
    SECRET_KEY,
    PEPPER,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    COOKIE_SECURE,
    COOKIE_SAMESITE,
)

_ph = PasswordHash.recommended()

REFRESH_COOKIE_NAME = "refresh_token"


def hash_password(plain: str) -> str:
    return _ph.hash(f"{plain}{PEPPER}")


def verify_password(plain: str, hashed: str) -> bool:
    return _ph.verify(f"{plain}{PEPPER}", hashed)


def create_access_token(user_id: int, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return jwt.encode(
        {"sub": str(user_id), "role": role, "exp": exp},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


def create_refresh_token() -> tuple[str, str, datetime]:
    raw_token = secrets.token_urlsafe(48)

    token_hash = hmac.new(
        SECRET_KEY.encode("utf-8"),
        raw_token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    return raw_token, token_hash, expires_at


def hash_refresh_token(raw_token: str) -> str:
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        raw_token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def set_refresh_cookie(
    response: Response,
    raw_token: str,
    expires_at: datetime,
) -> None:
    max_age = int(
        (expires_at - datetime.now(timezone.utc)).total_seconds()
    )

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=raw_token,
        max_age=max(max_age, 0),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/api/auth",
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/api/auth",
    )
