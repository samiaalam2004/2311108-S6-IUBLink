
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
PEPPER = os.getenv("PEPPER")
DATABASE_URL = os.getenv("DATABASE_URL")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = min(
    int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")),
    15
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)

COOKIE_SECURE = FRONTEND_URL.startswith("https://")
COOKIE_SAMESITE = "lax"

for name, value in (
    ("SECRET_KEY", SECRET_KEY),
    ("PEPPER", PEPPER),
    ("DATABASE_URL", DATABASE_URL),
):
    if not value:
        raise RuntimeError(
            f"{name} environment variable is not set"
        )
