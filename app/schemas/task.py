from typing import List
from pydantic import BaseModel, validator

from app.schemas.habit import HabitWithLog
from app.schemas.routine import RoutinePublic
from app.schemas.todo import TodoPublic
from app.schemas.validator import validate_date


class TaskPublic(BaseModel):
    todo_list: List[TodoPublic]
    routine_list: List[RoutinePublic]
    habit_list: List[HabitWithLog]


class TaskGetInput(BaseModel):
    date: str

    @validator("date")
    def validate_date(cls, date: str) -> str:
        return validate_date(date)
