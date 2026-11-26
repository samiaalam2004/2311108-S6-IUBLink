from database.connection import get_connection

ALLOWED_UPDATE_FIELDS = {"title", "description", "company"}


def create(data: dict, owner_id: int, owner_name: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO posts (title, description, post_type, company, owner_id, owner_name)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
                (data["title"], data["description"], data["post_type"],
                 data.get("company"), owner_id, owner_name),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def list_by_status(status: str) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM posts WHERE status = %s ORDER BY created_at DESC", (status,))
            return cur.fetchall()


def get_approved(post_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM posts WHERE id = %s AND status = 'approved'", (post_id,))
            return cur.fetchone()


def list_by_owner(owner_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM posts WHERE owner_id = %s ORDER BY created_at DESC", (owner_id,))
            return cur.fetchall()


def update_own(post_id: int, owner_id: int, changes: dict) -> dict | None:
    changes = {k: v for k, v in changes.items() if k in ALLOWED_UPDATE_FIELDS}
    assignments = ", ".join(f"{f} = %s" for f in changes)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE posts SET {assignments}, updated_at = NOW() "
                "WHERE id = %s AND owner_id = %s RETURNING *",
                list(changes.values()) + [post_id, owner_id],
            )
            row = cur.fetchone()
        conn.commit()
    return row


def delete_own(post_id: int, owner_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM posts WHERE id = %s AND owner_id = %s", (post_id, owner_id))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def review(post_id: int, status: str, note: str | None) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE posts SET status = %s, review_note = %s, updated_at = NOW() "
                "WHERE id = %s RETURNING *",
                (status, note, post_id),
            )
            row = cur.fetchone()
        conn.commit()
    return row