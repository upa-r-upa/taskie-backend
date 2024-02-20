from pydantic import BaseModel
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    order: int
    content: str = None

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

    completed: int = 0
