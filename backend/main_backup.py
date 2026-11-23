
import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Database setup
DB_PATH = Path(__file__).resolve().parent / "iublink.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                post_type TEXT NOT NULL,
                company TEXT,
                owner_id TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                owner_role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                review_note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


init_db()

app = FastAPI(title="IUBLink Career Management API")

# Allow React frontend to communicate with FastAPI
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


# Request models
class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    post_type: Literal["job_seeking", "job", "internship"]
    company: str | None = None
    owner_id: str
    owner_name: str
    owner_role: Literal["student", "alumni"]


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=10)
    company: str | None = None


class ReviewRequest(BaseModel):
    status: Literal["approved", "rejected"]
    review_note: str | None = None


# Health check
@app.get("/api/health")
def health():
    return {"status": "ok"}


# Create a career post
@app.post("/api/posts", status_code=201)
def create_post(post: PostCreate):
    if post.post_type == "job_seeking" and post.owner_role != "student":
        raise HTTPException(
            status_code=400,
            detail="Only students can create job-seeking posts",
        )

    if post.post_type in ("job", "internship") and post.owner_role != "alumni":
        raise HTTPException(
            status_code=400,
            detail="Only alumni can create job and internship opportunities",
        )

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO posts
            (title, description, post_type, company, owner_id, owner_name, owner_role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post.title,
                post.description,
                post.post_type,
                post.company,
                post.owner_id,
                post.owner_name,
                post.owner_role,
            ),
        )
        post_id = cursor.lastrowid
        row = conn.execute(
            "SELECT * FROM posts WHERE id = ?", (post_id,)
        ).fetchone()

    return dict(row)


# Read all approved posts
@app.get("/api/posts")
def get_approved_posts():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts WHERE status = 'approved' ORDER BY created_at DESC"
        ).fetchall()

    return [dict(row) for row in rows]


# Read a single approved post
@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM posts WHERE id = ? AND status = 'approved'",
            (post_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Approved post not found")

    return dict(row)


# Read posts belonging to one owner
@app.get("/api/my-posts")
def get_my_posts(owner_id: str):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts WHERE owner_id = ? ORDER BY created_at DESC",
            (owner_id,),
        ).fetchall()

    return [dict(row) for row in rows]


# Update your own post
@app.patch("/api/posts/{post_id}")
def update_post(post_id: int, owner_id: str, post: PostUpdate):
    changes = post.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=400, detail="No changes provided")

    allowed_fields = {"title", "description", "company"}
    if not set(changes).issubset(allowed_fields):
        raise HTTPException(status_code=400, detail="Invalid fields")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM posts WHERE id = ? AND owner_id = ?",
            (post_id, owner_id),
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Post not found")

        assignments = ", ".join(f"{field} = ?" for field in changes)
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
            "SELECT * FROM posts WHERE id = ?", (post_id,)
        ).fetchone()

    return dict(updated)


# Delete your own post
@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, owner_id: str):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM posts WHERE id = ? AND owner_id = ?",
            (post_id, owner_id),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully"}


# Admin: view posts by approval status
@app.get("/api/admin/posts")
def get_admin_posts(
    status: Literal["pending", "approved", "rejected"] = "pending",
):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts WHERE status = ? ORDER BY created_at DESC",
            (status,),
        ).fetchall()

    return [dict(row) for row in rows]


# Admin: approve or reject a post
@app.patch("/api/admin/posts/{post_id}/review")
def review_post(post_id: int, review: ReviewRequest):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE posts
            SET status = ?, review_note = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (review.status, review.review_note, post_id),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post not found")

        row = conn.execute(
            "SELECT * FROM posts WHERE id = ?", (post_id,)
        ).fetchone()

    return dict(row)


# Serve the built React frontend when available
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
