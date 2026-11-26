
from datetime import datetime

from database.connection import get_connection


def create_session(
    user_id: int,
    token_hash: str,
    expires_at: datetime,
) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.refresh_tokens
                    (user_id, token_hash, expires_at)
                VALUES (%s, %s, %s)
                """,
                (user_id, token_hash, expires_at),
            )


def get_session_by_token_hash(token_hash: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    rt.id,
                    rt.user_id,
                    rt.expires_at,
                    rt.revoked_at,
                    u.role,
                    u.is_banned
                FROM public.refresh_tokens AS rt
                JOIN public.users AS u ON u.id = rt.user_id
                WHERE rt.token_hash = %s
                """,
                (token_hash,),
            )
            return cur.fetchone()


def rotate_session(
    old_session_id: int,
    user_id: int,
    new_token_hash: str,
    expires_at: datetime,
) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE public.refresh_tokens
                SET revoked_at = NOW()
                WHERE id = %s
                  AND user_id = %s
                  AND revoked_at IS NULL
                  AND expires_at > NOW()
                RETURNING id
                """,
                (old_session_id, user_id),
            )

            if cur.fetchone() is None:
                return False

            cur.execute(
                """
                INSERT INTO public.refresh_tokens
                    (user_id, token_hash, expires_at)
                VALUES (%s, %s, %s)
                """,
                (user_id, new_token_hash, expires_at),
            )

    return True


def revoke_session_by_hash(token_hash: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE public.refresh_tokens
                SET revoked_at = NOW()
                WHERE token_hash = %s
                  AND revoked_at IS NULL
                """,
                (token_hash,),
            )


def revoke_all_sessions(user_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE public.refresh_tokens
                SET revoked_at = NOW()
                WHERE user_id = %s
                  AND revoked_at IS NULL
                """,
                (user_id,),
            )
