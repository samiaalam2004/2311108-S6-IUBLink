
from fastapi import HTTPException

from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from crud import user_crud, session_crud


def register(full_name: str, email: str, password: str) -> dict:
    email = email.lower()

    if user_crud.get_by_email(email):
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user_id = user_crud.create_user(
        full_name,
        email,
        hash_password(password),
    )

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "role": "user",
    }


def login(email: str, password: str) -> tuple[dict, str, object]:
    u = user_crud.get_by_email(email.lower())

    if u is None or not verify_password(
        password,
        u["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if u["is_banned"]:
        raise HTTPException(
            status_code=403,
            detail="Your account has been banned",
        )

    access_token = create_access_token(
        u["id"],
        u["role"],
    )

    raw_refresh_token, token_hash, expires_at = (
        create_refresh_token()
    )

    session_crud.create_session(
        u["id"],
        token_hash,
        expires_at,
    )

    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": u["id"],
            "full_name": u["full_name"],
            "email": u["email"],
            "role": u["role"],
        },
    }

    return response_data, raw_refresh_token, expires_at


def refresh_login(raw_refresh_token: str) -> tuple[str, str, object]:
    from auth.security import hash_refresh_token

    token_hash = hash_refresh_token(raw_refresh_token)

    session = session_crud.get_session_by_token_hash(token_hash)

    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if session["revoked_at"] is not None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has been revoked",
        )

    from datetime import datetime, timezone

    if session["expires_at"] <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired",
        )

    if session["is_banned"]:
        session_crud.revoke_session_by_hash(token_hash)
        raise HTTPException(
            status_code=403,
            detail="Your account has been banned",
        )

    new_raw_token, new_token_hash, expires_at = create_refresh_token()

    rotated = session_crud.rotate_session(
        session["id"],
        session["user_id"],
        new_token_hash,
        expires_at,
    )

    if not rotated:
        raise HTTPException(
            status_code=401,
            detail="Refresh token is no longer valid",
        )

    access_token = create_access_token(
        session["user_id"],
        session["role"],
    )

    return access_token, new_raw_token, expires_at

def logout(raw_refresh_token: str | None) -> None:
    if not raw_refresh_token:
        return

    from auth.security import hash_refresh_token

    token_hash = hash_refresh_token(raw_refresh_token)

    session_crud.revoke_session_by_hash(token_hash)

def logout_all(user_id: int) -> None:
    session_crud.revoke_all_sessions(user_id)
