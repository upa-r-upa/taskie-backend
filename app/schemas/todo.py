from pydantic import BaseModel
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    order: int
    target_date: datetime
    content: str = None

    class Config:
        orm_mode = True


class TodoCreateInput(TodoBase):
    pass


class TodoUpdateInput(BaseModel):
    title: str
    target_date: datetime
    completed: bool
    content: str = None


class TodoPublic(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    target_date: datetime
    completed_at: datetime | None

    class Config:
        orm_mode = True


class TodoOrderUpdate(BaseModel):
    id: int
    order: int


class TodoOrderUpdateInput(BaseModel):
    todo_list: list[TodoOrderUpdate]
