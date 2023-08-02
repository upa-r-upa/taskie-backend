from datetime import datetime
from pydantic import BaseModel
from typing import List


class RoutineBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    completed: bool
    active: bool
    title: str
    start_time_minutes: int
    repeat_days: List[int]

    class Config:
        orm_mode = True


class RoutineItemBase(BaseModel):
    title: str
    duration_minutes: int


class RoutineCreateInput(BaseModel):
    title: str
    start_time_minutes: int
    repeat_days: List[int]
    todo_items: List[RoutineItemBase]

    class Config:
        orm_mode = True


class RoutineItem(RoutineItemBase):
    id: int  # routine todo id
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RoutineDetail(RoutineBase):
    todo_items: List[RoutineItem]

    class Config:
        orm_mode = True
