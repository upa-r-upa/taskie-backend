from typing import List
from pydantic import BaseModel, validator

from app.schemas.habit import HabitWithLog
from app.schemas.routine import RoutineDetail
from app.schemas.todo import TodoDetail
from app.schemas.validator import validate_date


class TaskPublic(BaseModel):
    todo_list: List[TodoDetail]
    routine_list: List[RoutineDetail]
    habit_list: List[HabitWithLog]


class TaskGetInput(BaseModel):
    date: str

    @validator("date")
    def validate_date(cls, date: str) -> str:
        return validate_date(date)
