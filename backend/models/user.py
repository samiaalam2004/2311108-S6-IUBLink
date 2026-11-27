USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    ban_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""

USERS_ALTER_SQL = [
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS department TEXT",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS batch_or_graduation TEXT",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS headline TEXT",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS linkedin_url TEXT",
]