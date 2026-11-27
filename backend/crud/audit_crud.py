from database.connection import get_connection


def log(user_id: int | None, email: str | None, action: str,
        ip: str | None = None, ua: str | None = None, details: str | None = None) -> None:
    """audit log লিখতে গিয়ে error হলে মূল কাজ যেন না ভাঙে।"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO audit_logs (user_id, email, action, ip, user_agent, details)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (user_id, email, action, ip, ua, details),
                )
            conn.commit()
    except Exception as exc:  # noqa: BLE001
        print(f"audit log failed: {exc}")


def record_attempt(email: str, ip: str, success: bool) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO login_attempts (email, ip, success) VALUES (%s, %s, %s)",
                (email, ip, success),
            )
        conn.commit()


def count_recent_failures(email: str, minutes: int) -> int:
    """শেষ সফল login এর পর, শেষ N মিনিটের ব্যর্থ চেষ্টা।"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT COUNT(*) AS n FROM login_attempts
                   WHERE email = %s AND success = FALSE
                     AND created_at > NOW() - (%s * INTERVAL '1 minute')
                     AND created_at > COALESCE(
                         (SELECT MAX(created_at) FROM login_attempts
                          WHERE email = %s AND success = TRUE), '-infinity'::timestamptz)""",
                (email, minutes, email),
            )
            return cur.fetchone()["n"]