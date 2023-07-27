from pydantic import BaseModel, validator
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    content: str = None

    class Config:
        orm_mode = True


class TodoDetail(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
