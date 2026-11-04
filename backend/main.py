
import sqlite3
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal

import jwt
from pwdlib import PasswordHash

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, EmailStr


# ==========================================
# AUTHENTICATION CONFIGURATION
# ==========================================

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_PATH = Path("/tmp/iublink.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN ('student', 'alumni', 'faculty', 'admin')
                ),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                post_type TEXT NOT NULL CHECK (
                    post_type IN ('job_seeking', 'job', 'internship')
                ),
                company TEXT,
                owner_id TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                owner_role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending' CHECK (
                    status IN ('pending', 'approved', 'rejected')
                ),
                review_note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    # Optional first-admin bootstrap.
    # An account is created only when credentials are supplied
    # through environment variables and no admin exists.

    bootstrap_name = os.getenv("BOOTSTRAP_ADMIN_NAME")
    bootstrap_email = os.getenv("BOOTSTRAP_ADMIN_EMAIL")
    bootstrap_password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")

    if bootstrap_name and bootstrap_email and bootstrap_password:

        if len(bootstrap_password) < 8:
            raise RuntimeError(
                "Bootstrap admin password must be at least 8 characters"
            )

        with get_connection() as conn:

            existing_admin = conn.execute(
                "SELECT id FROM users WHERE role = 'admin' LIMIT 1"
            ).fetchone()

            if existing_admin is None:

                existing_email = conn.execute(
                    "SELECT id FROM users WHERE email = ?",
                    (bootstrap_email.lower(),),
                ).fetchone()

                if existing_email:
                    raise RuntimeError(
                        "Bootstrap admin email already belongs to another account"
                    )

                conn.execute(
                    """
                    INSERT INTO users
                    (full_name, email, password_hash, role)
                    VALUES (?, ?, ?, 'admin')
                    """,
                    (
                        bootstrap_name,
                        bootstrap_email.lower(),
                        password_hash.hash(bootstrap_password),
                    ),
                )

                conn.commit()

                print("Initial admin account created successfully.")


init_db()


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="IUBLink Career Management API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODELS
# ==========================================

class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["student", "alumni", "faculty", "admin"]


class AdminUserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["faculty", "admin"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    post_type: Literal["job_seeking", "job", "internship"]
    company: str | None = None


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=10)
    company: str | None = None


class ReviewRequest(BaseModel):
    status: Literal["approved", "rejected"]
    review_note: str | None = None


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health():
    return {"status": "ok"}


# ==========================================
# JWT ACCESS TOKEN
# ==========================================

def create_access_token(user_id: int, role: str):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==========================================
# USER REGISTRATION
# ==========================================

@app.post("/api/auth/register", status_code=201)
def register_user(user: UserRegister):

    # Public registration is only for students and alumni.
    # Faculty and admin accounts must be created by an admin.

    if user.role not in ("student", "alumni"):
        raise HTTPException(
            status_code=403,
            detail="Faculty and Admin accounts must be created by an administrator",
        )

    hashed_password = password_hash.hash(user.password)

    with get_connection() as conn:

        existing_user = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (str(user.email).lower(),),
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        cursor = conn.execute(
            """
            INSERT INTO users
            (full_name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.full_name,
                str(user.email).lower(),
                hashed_password,
                user.role,
            ),
        )

        user_id = cursor.lastrowid
        conn.commit()

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "full_name": user.full_name,
        "email": str(user.email).lower(),
        "role": user.role,
    }


# ==========================================
# GET CURRENT USER
# ==========================================

def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception

    with get_connection() as conn:

        user = conn.execute(
            """
            SELECT id, full_name, email, role
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if user is None:
        raise credentials_exception

    return dict(user)


# ==========================================
# ROLE-BASED ACCESS CONTROL
# ==========================================

def require_role(*allowed_roles):

    def role_checker(
        current_user: dict = Depends(get_current_user),
    ):

        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker


# ==========================================
# ADMIN: CREATE FACULTY / ADMIN ACCOUNT
# ==========================================

@app.post("/api/admin/users", status_code=201)
def create_staff_user(
    user: AdminUserCreate,
    current_user: dict = Depends(require_role("admin")),
):

    hashed_password = password_hash.hash(user.password)

    with get_connection() as conn:

        existing_user = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (str(user.email).lower(),),
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        cursor = conn.execute(
            """
            INSERT INTO users
            (full_name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.full_name,
                str(user.email).lower(),
                hashed_password,
                user.role,
            ),
        )

        user_id = cursor.lastrowid
        conn.commit()

    return {
        "message": "Staff account created successfully",
        "user_id": user_id,
        "full_name": user.full_name,
        "email": str(user.email).lower(),
        "role": user.role,
    }


# ==========================================
# USER LOGIN
# ==========================================

@app.post("/api/auth/login")
def login_user(user: UserLogin):

    with get_connection() as conn:

        existing_user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (str(user.email).lower(),),
        ).fetchone()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not password_hash.verify(
        user.password,
        existing_user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=existing_user["id"],
        role=existing_user["role"],
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": existing_user["id"],
            "full_name": existing_user["full_name"],
            "email": existing_user["email"],
            "role": existing_user["role"],
        },
    }


# ==========================================
# CURRENT USER API
# ==========================================

@app.get("/api/auth/me")
def read_current_user(
    current_user: dict = Depends(get_current_user),
):
    return current_user


# ==========================================
# CREATE A CAREER POST
# ==========================================

@app.post("/api/posts", status_code=201)
def create_post(
    post: PostCreate,
    current_user: dict = Depends(get_current_user),
):

    user_role = current_user["role"]

    if post.post_type == "job_seeking" and user_role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can create job-seeking posts",
        )

    if post.post_type in ("job", "internship") and user_role != "alumni":
        raise HTTPException(
            status_code=403,
            detail="Only alumni can create job and internship opportunities",
        )

    with get_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO posts
            (
                title, description, post_type, company,
                owner_id, owner_name, owner_role
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post.title,
                post.description,
                post.post_type,
                post.company,
                str(current_user["id"]),
                current_user["full_name"],
                user_role,
            ),
        )

        post_id = cursor.lastrowid

        row = conn.execute(
            "SELECT * FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()

        conn.commit()

    return dict(row)


# ==========================================
# READ ALL APPROVED POSTS
# ==========================================

@app.get("/api/posts")
def get_approved_posts():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT * FROM posts
            WHERE status = 'approved'
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


# ==========================================
# READ SINGLE APPROVED POST
# ==========================================

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT * FROM posts
            WHERE id = ? AND status = 'approved'
            """,
            (post_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Approved post not found",
        )

    return dict(row)


# ==========================================
# READ MY POSTS
# ==========================================

@app.get("/api/my-posts")
def get_my_posts(
    current_user: dict = Depends(get_current_user),
):

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT * FROM posts
            WHERE owner_id = ?
            ORDER BY created_at DESC
            """,
            (str(current_user["id"]),),
        ).fetchall()

    return [dict(row) for row in rows]


# ==========================================
# UPDATE OWN POST
# ==========================================

@app.patch("/api/posts/{post_id}")
def update_post(
    post_id: int,
    post: PostUpdate,
    current_user: dict = Depends(get_current_user),
):

    changes = post.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="No changes provided",
        )

    owner_id = str(current_user["id"])

    with get_connection() as conn:

        existing = conn.execute(
            """
            SELECT * FROM posts
            WHERE id = ? AND owner_id = ?
            """,
            (post_id, owner_id),
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        assignments = ", ".join(
            f"{field} = ?" for field in changes
        )

        values = list(changes.values())
        values.extend([post_id, owner_id])

        conn.execute(
            f"""
            UPDATE posts
            SET {assignments}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND owner_id = ?
            """,
            values,
        )

        updated = conn.execute(
            "SELECT * FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()

        conn.commit()

    return dict(updated)


# ==========================================
# DELETE OWN POST
# ==========================================

@app.delete("/api/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user),
):

    owner_id = str(current_user["id"])

    with get_connection() as conn:

        cursor = conn.execute(
            """
            DELETE FROM posts
            WHERE id = ? AND owner_id = ?
            """,
            (post_id, owner_id),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        conn.commit()

    return {
        "message": "Post deleted successfully"
    }


# ==========================================
# ADMIN: VIEW POSTS BY STATUS
# ==========================================

@app.get("/api/admin/posts")
def get_admin_posts(
    status: Literal["pending", "approved", "rejected"] = "pending",
    current_user: dict = Depends(require_role("admin")),
):

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT * FROM posts
            WHERE status = ?
            ORDER BY created_at DESC
            """,
            (status,),
        ).fetchall()

    return [dict(row) for row in rows]


# ==========================================
# ADMIN: APPROVE OR REJECT POST
# ==========================================

@app.patch("/api/admin/posts/{post_id}/review")
def review_post(
    post_id: int,
    review: ReviewRequest,
    current_user: dict = Depends(require_role("admin")),
):

    with get_connection() as conn:

        cursor = conn.execute(
            """
            UPDATE posts
            SET status = ?,
                review_note = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                review.status,
                review.review_note,
                post_id,
            ),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        row = conn.execute(
            "SELECT * FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()

        conn.commit()

    return dict(row)


# ==========================================
# SERVE FRONTEND BUILD
# ==========================================

FRONTEND_DIR = (
    Path(__file__).resolve().parent.parent
    / "frontend"
    / "dist"
)

if FRONTEND_DIR.is_dir():
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )
