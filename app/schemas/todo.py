from pydantic import BaseModel, validator
from datetime import datetime

from app.schemas.validator import validate_date


class TodoBase(BaseModel):
    title: str
    order: int
    target_date: str
    content: str = None

    class Config:
        orm_mode = True


class TodoUpdateInput(BaseModel):
    title: str
    target_date: str
    content: str = None

    @validator("target_date")
    def validate_target_date(cls, v):
        return validate_date(v)


class TodoDetail(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    target_date: datetime

    class Config:
        orm_mode = True


class TodoOrderUpdate(BaseModel):
    id: int
    order: int


class TodoOrderUpdateInput(BaseModel):
    todo_list: list[TodoOrderUpdate]


class TodoListGetInput(BaseModel):
    limit: int
    offset: int

    start_date: str = None
    end_date: str = None

    completed: bool = False
