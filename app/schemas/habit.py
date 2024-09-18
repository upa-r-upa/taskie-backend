from datetime import date, datetime
from typing import List
from fastapi.params import Query
from pydantic import BaseModel, validator

from app.api.errors import (
    DUPLICATED_VALUE,
    INVALID_VALUE_RANGE,
    VALUE_MUST_NOT_BE_EMPTY,
    VALUE_TOO_LONG,
)
from app.models.models import Habit
from app.schemas.common import ListLoadParams


class HabitBase(BaseModel):
    title: str
    start_time_minutes: int
    end_time_minutes: int
    repeat_time_minutes: int
    repeat_days: list[int]

    class Config:
        orm_mode = True


class HabitModifiableBase(HabitBase):
    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) > 255:
            raise ValueError(VALUE_TOO_LONG)
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v > 1440:
            raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("end_time_minutes")
    def validate_end_time_minutes(cls, v):
        if v < 0 or v > 1440:
            raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) != len(set(v)):
            raise ValueError(DUPLICATED_VALUE)

        for i in range(len(v)):
            if v[i] < 0 or v[i] > 6:
                raise ValueError(INVALID_VALUE_RANGE)

        if v != sorted(v):
            v = sorted(v)

        return v


class HabitUpdateInput(HabitModifiableBase):
    activated: bool | None


class HabitCreateInput(HabitModifiableBase):
    pass


class HabitPublic(HabitBase):
    id: int
    activated: bool
    created_at: datetime
    updated_at: datetime

    @validator("repeat_days", pre=True)
    def parsed_repeat_days(cls, v):
        if isinstance(v, str):
            return [int(day) for day in v]
        return v

    class Config:
        orm_mode = True


class HabitListGetParams(ListLoadParams):
    log_target_date: date = Query()
    activated: bool | None = Query(True)


class HabitLog(BaseModel):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True


class HabitWithLog(HabitPublic):
    near_weekday: int
    log_list: List[HabitLog]

    @classmethod
    def from_orm_with_weekday(
        cls, db_obj: Habit, log_list: list[HabitLog], today_weekday: int
    ):
        habit = HabitPublic.from_orm(db_obj).dict()
        habit_with_log = HabitWithLog(
            **habit,
            near_weekday=HabitWithLog.calculate_near_weekday(
                habit["repeat_days"], today_weekday
            ),
            log_list=log_list
        )

        return habit_with_log

    @classmethod
    def calculate_near_weekday(
        cls, repeat_days: list[int], curr_week: int
    ) -> int:
        for day in repeat_days:
            if day >= curr_week:
                return day
        return repeat_days[0]
