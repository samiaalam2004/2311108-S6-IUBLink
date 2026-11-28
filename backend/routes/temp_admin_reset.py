
import os
import secrets

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from database.connection import get_connection
from auth.security import hash_password

router = APIRouter(tags=["Temporary Admin Password Reset"])


class AdminPasswordResetRequest(BaseModel):
    email: str
    new_password: str = Field(min_length=12, max_length=128)


@router.post("/api/temporary/admin-password-reset")
def reset_admin_password(
    payload: AdminPasswordResetRequest,
    reset_key: str = Header(..., alias="X-Reset-Key"),
):
    configured_key = os.getenv("ADMIN_PASSWORD_RESET_KEY")

    if not configured_key:
        raise HTTPException(status_code=503, detail="Reset is not configured")

    if not secrets.compare_digest(reset_key, configured_key):
        raise HTTPException(status_code=403, detail="Invalid reset key")

    email = payload.email.strip().lower()
    password_hash = hash_password(payload.new_password)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET password_hash = %s
                WHERE LOWER(email) = %s
                  AND role = 'admin'
                RETURNING id, email
                """,
                (password_hash, email),
            )
            user = cur.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    return {
        "message": "Admin password updated successfully",
        "email": user["email"]
    }
