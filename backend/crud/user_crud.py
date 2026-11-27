from database.connection import get_connection

PROFILE_FIELDS = {
    "full_name", "department", "batch_or_graduation",
    "headline", "bio", "linkedin_url",
}


def get_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, full_name, email, role, is_banned, ban_reason, created_at,
                          department, batch_or_graduation, headline, bio, linkedin_url
                   FROM users WHERE id = %s""",
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


def update_profile(user_id: int, changes: dict) -> dict | None:
    changes = {k: v for k, v in changes.items() if k in PROFILE_FIELDS}
    if changes:
        assignments = ", ".join(f"{f} = %s" for f in changes)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE users SET {assignments} WHERE id = %s",
                    list(changes.values()) + [user_id],
                )
                if "full_name" in changes:
                    cur.execute(
                        "UPDATE posts SET owner_name = %s WHERE owner_id = %s",
                        (changes["full_name"], user_id),
                    )
            conn.commit()
    return get_by_id(user_id)


def update_password(user_id: int, password_hash: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (password_hash, user_id),
            )
        conn.commit()