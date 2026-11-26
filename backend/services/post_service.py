from fastapi import HTTPException
from crud import post_crud


def create_post(data: dict, user: dict) -> dict:
    return post_crud.create(data, user["id"], user["full_name"])


def list_approved() -> list[dict]:
    return post_crud.list_by_status("approved")


def get_approved_or_404(post_id: int) -> dict:
    post = post_crud.get_approved(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Approved post not found")
    return post


def my_posts(user_id: int) -> list[dict]:
    return post_crud.list_by_owner(user_id)


def update_own_post(post_id: int, user_id: int, changes: dict) -> dict:
    if not changes:
        raise HTTPException(status_code=400, detail="No changes provided")
    post = post_crud.update_own(post_id, user_id, changes)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def delete_own_post(post_id: int, user_id: int) -> dict:
    if not post_crud.delete_own(post_id, user_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}


def review_post(post_id: int, status: str, note: str | None) -> dict:
    post = post_crud.review(post_id, status, note)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

def list_by_status(status: str) -> list[dict]:
    return post_crud.list_by_status(status)