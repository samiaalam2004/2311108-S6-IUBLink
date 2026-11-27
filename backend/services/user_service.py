from fastapi import HTTPException

from auth.security import hash_password, verify_password, hash_token
from crud import user_crud, session_crud, audit_crud


def update_profile(user: dict, changes: dict, ip: str, ua: str) -> dict:
    changes = {k: v for k, v in changes.items() if not (k == "full_name" and v is None)}

    changes = {k: (v.strip() or None) if isinstance(v, str) and k != "full_name" else v
               for k, v in changes.items()}
    updated = user_crud.update_profile(user["id"], changes)
    audit_crud.log(user["id"], user["email"], "profile_update", ip, ua)
    return updated


def change_password(user: dict, current: str, new: str, ip: str, ua: str) -> dict:
    record = user_crud.get_by_email(user["email"])
    if record is None or not verify_password(current, record["password_hash"]):
        audit_crud.log(user["id"], user["email"], "password_change_failed", ip, ua)
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if current == new:
        raise HTTPException(status_code=400,
                            detail="New password must be different from the current one")

    user_crud.update_password(user["id"], hash_password(new))
    session_crud.revoke_all_for_user(user["id"])
    audit_crud.log(user["id"], user["email"], "password_change", ip, ua)
    return {"message": "Password changed. Please log in again."}


def list_sessions(user_id: int, current_raw_token: str | None) -> list[dict]:
    current_hash = hash_token(current_raw_token) if current_raw_token else None
    return [
        {
            "id": s["id"], "ip": s["ip"], "user_agent": s["user_agent"],
            "created_at": s["created_at"], "last_used_at": s["last_used_at"],
            "expires_at": s["expires_at"],
            "is_current": s["token_hash"] == current_hash,
        }
        for s in session_crud.list_active(user_id)
    ]


def revoke_session(user: dict, session_id: int, ip: str, ua: str) -> dict:

    if not session_crud.revoke_one(session_id, user["id"]):
        raise HTTPException(status_code=404, detail="Session not found")
    audit_crud.log(user["id"], user["email"], "session_revoked", ip, ua,
                   details=f"session_id={session_id}")
    return {"message": "Session revoked"}