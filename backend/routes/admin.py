from typing import Literal
from fastapi import APIRouter, Depends

from auth.permissions import require_role, Role
from schemas.post import ReviewRequest
from services import post_service

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/posts")
def admin_posts(status: Literal["pending", "approved", "rejected"] = "pending",
                admin: dict = Depends(require_role(Role.ADMIN))):
    return post_service.list_by_status(status)

@router.patch("/posts/{post_id}/review")
def review(post_id: int, body: ReviewRequest, admin: dict = Depends(require_role(Role.ADMIN))):
    return post_service.review_post(post_id, body.status, body.review_note)