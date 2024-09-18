from typing import List
from pydantic import BaseModel

from app.schemas.habit import HabitWithLog
from app.schemas.routine import RoutinePublic
from app.schemas.todo import TodoPublic


class TaskPublic(BaseModel):
    todo_list: List[TodoPublic]
    routine_list: List[RoutinePublic]
    habit_list: List[HabitWithLog]
