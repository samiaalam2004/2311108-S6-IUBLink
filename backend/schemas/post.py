from typing import Literal
from pydantic import BaseModel, Field


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