from pydantic import BaseModel, validator
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    content: str = None

    class Config:
        orm_mode = True

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Title must not be empty")
        return v


class TodoDetail(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
