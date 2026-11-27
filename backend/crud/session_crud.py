from datetime import datetime

from database.connection import get_connection


def create(user_id: int, token_hash: str, ip: str, ua: str, expires_at: datetime) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO sessions (user_id, token_hash, ip, user_agent, expires_at)
                   VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                (user_id, token_hash, ip, ua, expires_at),
            )
            sid = cur.fetchone()["id"]
        conn.commit()
    return sid


def get_by_hash(token_hash: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM sessions WHERE token_hash = %s", (token_hash,))
            return cur.fetchone()


def rotate(session_id: int, new_hash: str, expires_at: datetime, ip: str, ua: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE sessions
                   SET token_hash = %s, expires_at = %s, ip = %s, user_agent = %s,
                       last_used_at = NOW()
                   WHERE id = %s""",
                (new_hash, expires_at, ip, ua, session_id),
            )
        conn.commit()


def revoke_by_hash(token_hash: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE sessions SET revoked_at = NOW() "
                "WHERE token_hash = %s AND revoked_at IS NULL",
                (token_hash,),
            )
        conn.commit()


def revoke_one(session_id: int, user_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE sessions SET revoked_at = NOW() "
                "WHERE id = %s AND user_id = %s AND revoked_at IS NULL",
                (session_id, user_id),
            )
            ok = cur.rowcount > 0
        conn.commit()
    return ok


def revoke_all_for_user(user_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE sessions SET revoked_at = NOW() "
                "WHERE user_id = %s AND revoked_at IS NULL",
                (user_id,),
            )
        conn.commit()


def list_active(user_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, token_hash, ip, user_agent, created_at, last_used_at, expires_at
                   FROM sessions
                   WHERE user_id = %s AND revoked_at IS NULL AND expires_at > NOW()
                   ORDER BY last_used_at DESC""",
                (user_id,),
            )
            return cur.fetchall()