from datetime import datetime
from pydantic import BaseModel, validator
from typing import List


class RoutineItemBase(BaseModel):
    title: str
    order: int
    duration_minutes: int


class RoutineCreateInput(BaseModel):
    title: str
    start_time_minutes: int
    repeat_days: List[int]
    routine_items: List[RoutineItemBase]

    class Config:
        orm_mode = True

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError("repeat_days must not be empty")
        for day in v:
            if day not in range(1, 8):
                raise ValueError(
                    "repeat_days must be a list of integers between 1 and 7"
                )
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError("start_time_minutes must be between 0 and 1439")
        return v

    @validator("routine_items")
    def validate_routine_items(cls, v):
        for item in v:
            if item.duration_minutes < 0:
                raise ValueError("duration_minutes must be positive")
            elif item.duration_minutes > 1440:
                raise ValueError("duration_minutes must be less than 1440")
        return v

    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError("title must not be empty")
        elif len(v) > 255:
            raise ValueError("title must be less than 255 characters")
        return v

    @validator("routine_items")
    def validate_routine_items_order(cls, v):
        order_list = []
        for item in v:
            order_list.append(item.order)
        order_list.sort()
        for i in range(len(order_list)):
            if order_list[i] != i + 1:
                raise ValueError("routine_items order must be 1, 2, 3, ...")
        return v


class RoutineItem(RoutineItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed: bool

    class Config:
        orm_mode = True


class RoutineBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    start_time_minutes: int
    repeat_days: List[int]

    class Config:
        orm_mode = True


class RoutineDetail(RoutineBase):
    routine_items: List[RoutineItem]

    class Config:
        orm_mode = True
