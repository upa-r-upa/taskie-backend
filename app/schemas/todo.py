from pydantic import BaseModel, validator
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    order: int
    content: str = None

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Title must not be empty")
        return v

    class Config:
        orm_mode = True


class TodoUpdateInput(BaseModel):
    title: str
    content: str = None


class TodoDetail(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

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
