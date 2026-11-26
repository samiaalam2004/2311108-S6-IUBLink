from database.connection import get_connection


def get_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, full_name, email, role, is_banned FROM users WHERE id = %s",
                (user_id,),
            )
            return cur.fetchone()


def get_by_email(email: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()


def create_user(full_name: str, email: str, password_hash: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (full_name, email, password_hash, role) "
                "VALUES (%s, %s, %s, 'user') RETURNING id",
                (full_name, email, password_hash),
            )
            user_id = cur.fetchone()["id"]
        conn.commit()
    return user_id