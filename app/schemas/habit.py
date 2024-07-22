from datetime import datetime
from typing import List
from fastapi.params import Query
from pydantic import BaseModel, validator

from app.api.errors import (
    DUPLICATED_VALUE,
    INVALID_VALUE_RANGE,
    VALUE_MUST_NOT_BE_EMPTY,
    VALUE_TOO_LONG,
)
from app.schemas.common import ListLoadParams
from app.schemas.validator import validate_date


class HabitBase(BaseModel):
    title: str
    start_time_minutes: int
    end_time_minutes: int
    repeat_time_minutes: int
    repeat_days: list[int]

    class Config:
        orm_mode = True


class HabitCreateInput(HabitBase):
    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) > 255:
            raise ValueError(VALUE_TOO_LONG)
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("end_time_minutes")
    def validate_end_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError(INVALID_VALUE_RANGE)
        return v

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError(VALUE_MUST_NOT_BE_EMPTY)
        elif len(v) != len(set(v)):
            raise ValueError(DUPLICATED_VALUE)

        for i in range(len(v)):
            if v[i] < 1 or v[i] > 7:
                raise ValueError(INVALID_VALUE_RANGE)

        if v != sorted(v):
            v = sorted(v)

        return v


class HabitDetail(HabitBase):
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
    log_target_date: str = Query(
        description="YYYY-MM-DD",
    )
    deleted: bool | None = Query(False)
    activated: bool | None = Query(True)

    @validator("log_target_date")
    def validate_log_target_date(cls, v):
        return validate_date(v)


class HabitLog(BaseModel):
    id: int
    completed_at: datetime

    class Config:
        orm_mode = True


class HabitWithLog(HabitDetail):
    log_list: List[HabitLog]

    class Config:
        orm_mode = True
