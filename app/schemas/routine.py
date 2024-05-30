from datetime import datetime
from pydantic import BaseModel, validator
from typing import List

from app.models.models import Routine, RoutineElement


class RoutineItemBase(BaseModel):
    title: str
    duration_minutes: int


class RoutineCreateInput(BaseModel):
    title: str
    start_time_minutes: int
    repeat_days: List[int]
    routine_elements: List[RoutineItemBase]

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError("repeat_days must contain at least one value")
        elif len(v) != len(set(v)):
            raise ValueError("repeat_days must not contain duplicate values")

        for i in range(len(v)):
            if v[i] < 1 or v[i] > 7:
                raise ValueError("repeat_days must be between 1 and 7")
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError("start_time_minutes must be between 0 and 1439")
        return v

    @validator("routine_elements")
    def validate_routine_elements(cls, v):
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

    class Config:
        orm_mode = True


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


class RoutineDetail(RoutineBase):
    deleted_at: datetime | None

    routine_elements: List[RoutineItem]

    def from_routine(routine: Routine, routine_elements: List[RoutineElement]):
        return RoutineDetail(
            id=routine.id,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=routine.repeat_days_to_list(),
            created_at=routine.created_at,
            updated_at=routine.updated_at,
            deleted_at=routine.deleted_at,
            routine_elements=[
                RoutineItem(
                    id=item.id,
                    title=item.title,
                    duration_minutes=item.duration_minutes,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                    completed=False,
                )
                for item in routine_elements
            ],
        )


class RoutineItemUpdate(RoutineItemBase):
    id: int | None


class RoutineUpdateInput(BaseModel):
    title: str | None
    start_time_minutes: int | None
    repeat_days: List[int] | None

    routine_elements: List[RoutineItemUpdate] | None


class RoutineItemCompleteUpdate(BaseModel):
    completed: bool
    item_ids: List[int]
