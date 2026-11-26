import os
import psycopg
from psycopg.rows import dict_row

from config.settings import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db():
    from models import ALL_TABLES
    from auth.security import hash_password

    with get_connection() as conn:
        with conn.cursor() as cur:
            for sql in ALL_TABLES:
                cur.execute(sql)
        conn.commit()

    name = os.getenv("BOOTSTRAP_ADMIN_NAME")
    email = os.getenv("BOOTSTRAP_ADMIN_EMAIL")
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")
    if not (name and email and password):
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO users (full_name, email, password_hash, role) "
                    "VALUES (%s, %s, %s, 'admin') ON CONFLICT (email) DO NOTHING",
                    (name, email.lower(), hash_password(password)),
                )
        conn.commit()