from datetime import datetime
from pydantic import BaseModel, validator
from typing import List

from app.api.errors import (
    DUPLICATED_VALUE,
    INVALID_VALUE_RANGE,
    VALUE_MUST_NOT_BE_EMPTY,
    VALUE_TOO_LONG,
)
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
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) != len(set(v)):
            raise ValueError(DUPLICATED_VALUE)

        for i in range(len(v)):
            if v[i] < 0 or v[i] > 6:
                raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("routine_elements")
    def validate_routine_elements(cls, v):
        for item in v:
            if item.duration_minutes < 0:
                raise ValueError(INVALID_VALUE_RANGE)
            elif item.duration_minutes > 1440:
                raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) > 255:
            raise ValueError(VALUE_TOO_LONG)
        return v

    class Config:
        orm_mode = True


class RoutineItem(RoutineItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    completed_at: datetime | None
    completed_duration_minutes: int | None

    class Config:
        orm_mode = True

    def from_routine_element(element: RoutineElement, completed_at: datetime):
        return RoutineItem(
            id=element.id,
            title=element.title,
            duration_minutes=element.duration_minutes,
            created_at=element.created_at,
            updated_at=element.updated_at,
            completed_at=completed_at,
        )


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

    def from_routine_with_log(
        routine: Routine, routine_items: List[RoutineItem]
    ):
        return RoutineDetail(
            id=routine.id,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=routine.repeat_days_to_list(),
            created_at=routine.created_at,
            updated_at=routine.updated_at,
            deleted_at=routine.deleted_at,
            routine_elements=routine_items,
        )

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


class RoutineLogBase(BaseModel):
    routine_item_id: int
    duration_minutes: int
    is_skipped: bool = False


class RoutineLogPutInput(BaseModel):
    logs: List[RoutineLogBase]
