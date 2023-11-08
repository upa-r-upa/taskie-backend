from datetime import datetime
from pydantic import BaseModel
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
