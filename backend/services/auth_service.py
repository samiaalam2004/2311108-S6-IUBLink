from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from auth.security import (
    hash_password, verify_password, create_access_token,
    generate_refresh_token, hash_token,
)
from config.settings import REFRESH_TOKEN_EXPIRE_DAYS, MAX_FAILED_ATTEMPTS, LOCKOUT_MINUTES
from crud import user_crud, session_crud, audit_crud


def _refresh_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)


def _public_user(u: dict) -> dict:
    return {"id": u["id"], "full_name": u["full_name"],
            "email": u["email"], "role": u["role"]}


def register(full_name: str, email: str, password: str, ip: str, ua: str) -> dict:
    email = email.lower()
    if user_crud.get_by_email(email):
        raise HTTPException(status_code=409, detail="Email already registered")
    user_id = user_crud.create_user(full_name, email, hash_password(password))
    audit_crud.log(user_id, email, "register", ip, ua)
    return {"message": "User registered successfully", "user_id": user_id,
            "full_name": full_name, "email": email, "role": "user"}


def login(email: str, password: str, ip: str, ua: str) -> tuple[dict, str]:
    email = email.lower()

    # brute-force protection
    if audit_crud.count_recent_failures(email, LOCKOUT_MINUTES) >= MAX_FAILED_ATTEMPTS:
        audit_crud.log(None, email, "login_locked", ip, ua)
        raise HTTPException(
            status_code=429,
            detail=f"Too many failed attempts. Try again in {LOCKOUT_MINUTES} minutes.",
        )

    u = user_crud.get_by_email(email)
    if u is None or not verify_password(password, u["password_hash"]):
        audit_crud.record_attempt(email, ip, False)
        audit_crud.log(u["id"] if u else None, email, "login_failed", ip, ua)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if u["is_banned"]:
        audit_crud.log(u["id"], email, "login_blocked_banned", ip, ua)
        raise HTTPException(status_code=403, detail="Your account has been banned")

    audit_crud.record_attempt(email, ip, True)

    raw_refresh = generate_refresh_token()
    session_crud.create(u["id"], hash_token(raw_refresh), ip, ua, _refresh_expiry())
    audit_crud.log(u["id"], email, "login", ip, ua)

    return {
        "access_token": create_access_token(u["id"], u["role"]),
        "token_type": "bearer",
        "user": _public_user(u),
    }, raw_refresh


def refresh(raw_token: str | None, ip: str, ua: str) -> tuple[dict, str]:
    invalid = HTTPException(status_code=401, detail="Invalid or expired refresh token")
    if not raw_token:
        raise invalid

    session = session_crud.get_by_hash(hash_token(raw_token))
    if (session is None or session["revoked_at"] is not None
            or session["expires_at"] <= datetime.now(timezone.utc)):
        raise invalid

    user = user_crud.get_by_id(session["user_id"])
    if user is None:
        raise invalid
    if user["is_banned"]:
        session_crud.revoke_by_hash(session["token_hash"])
        raise HTTPException(status_code=403, detail="Your account has been banned")

    # rotation: পুরনো token বাতিল, নতুন token
    new_raw = generate_refresh_token()
    session_crud.rotate(session["id"], hash_token(new_raw), _refresh_expiry(), ip, ua)

    return {
        "access_token": create_access_token(user["id"], user["role"]),
        "token_type": "bearer",
        "user": _public_user(user),
    }, new_raw


def logout(raw_token: str | None, ip: str, ua: str) -> dict:
    if raw_token:
        token_hash = hash_token(raw_token)
        session = session_crud.get_by_hash(token_hash)
        session_crud.revoke_by_hash(token_hash)
        if session:
            user = user_crud.get_by_id(session["user_id"])
            audit_crud.log(session["user_id"], user["email"] if user else None,
                           "logout", ip, ua)
    return {"message": "Logged out"}