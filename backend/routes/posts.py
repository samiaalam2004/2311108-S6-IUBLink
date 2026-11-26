from fastapi import APIRouter, Depends

from auth.permissions import get_current_user
from schemas.post import PostCreate, PostUpdate
from services import post_service

router = APIRouter(prefix="/api", tags=["posts"])


@router.post("/posts", status_code=201)
def create_post(body: PostCreate, user: dict = Depends(get_current_user)):
    return post_service.create_post(body.model_dump(), user)


@router.get("/posts")
def list_posts():
    return post_service.list_approved()


@router.get("/posts/{post_id}")
def get_post(post_id: int):
    return post_service.get_approved_or_404(post_id)


@router.get("/my-posts")
def my_posts(user: dict = Depends(get_current_user)):
    return post_service.my_posts(user["id"])


@router.patch("/posts/{post_id}")
def update_post(post_id: int, body: PostUpdate, user: dict = Depends(get_current_user)):
    return post_service.update_own_post(post_id, user["id"], body.model_dump(exclude_unset=True))


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, user: dict = Depends(get_current_user)):
    return post_service.delete_own_post(post_id, user["id"])