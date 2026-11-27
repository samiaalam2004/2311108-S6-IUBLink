
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

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
MAX_FAILED_ATTEMPTS = int(os.getenv("MAX_FAILED_ATTEMPTS", "5"))
LOCKOUT_MINUTES = int(os.getenv("LOCKOUT_MINUTES", "15"))

REFRESH_COOKIE_NAME = "refresh_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax").lower()  # lax | none | strict