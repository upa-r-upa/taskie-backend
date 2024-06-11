from datetime import datetime
from pydantic import BaseModel, validator

from app.models.models import Habit


class HabitBase(BaseModel):
    title: str
    start_time_minutes: int
    end_time_minutes: int
    repeat_time_minutes: int
    repeat_days: list[int]


class HabitCreateInput(HabitBase):
    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError("title must not be empty")
        elif len(v) > 255:
            raise ValueError("title must be less than 255 characters")
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError("start_time_minutes must be between 0 and 1439")
        return v

    @validator("end_time_minutes")
    def validate_end_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError("end_time_minutes must be between 0 and 1439")
        return v

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError("repeat_days must contain at least one value")
        elif len(v) != len(set(v)):
            raise ValueError("repeat_days must not contain duplicate values")

        for i in range(len(v)):
            if v[i] < 1 or v[i] > 7:
                raise ValueError("repeat_days must be between 1 and 7")

        if v != sorted(v):
            v = sorted(v)

        return v


class HabitDetail(BaseModel):
    id: int
    title: str
    start_time_minutes: int
    repeat_time_minutes: int
    repeat_days: list[int]
    active: bool
    created_at: datetime
    updated_at: datetime

    def from_habit(habit: Habit):
        return HabitDetail(
            id=habit.id,
            title=habit.title,
            start_time_minutes=habit.start_time_minutes,
            repeat_time_minutes=habit.repeat_time_minutes,
            repeat_days=habit.repeat_days_to_list(),
            active=habit.active,
            created_at=habit.created_at,
            updated_at=habit.updated_at,
        )
