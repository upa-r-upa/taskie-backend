from datetime import date
from pytest import Session
from .base import ProtectedBaseRepository

from app.api.dao.todo_dao import TodoDAO
from .routine_repository import RoutineRepository
from .habit_repository import HabitRepository
from app.schemas.task import TaskPublic


class TaskRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user_id: int):
        super().__init__(db, user_id)

        self.routine_repository = RoutineRepository(db=db, user_id=user_id)
        self.todo_dao = TodoDAO(db=db, user_id=user_id)
        self.habit_repository = HabitRepository(db=db, user_id=user_id)

    def get_all_task_by_date(self, date: date) -> TaskPublic:
        todo_list = self.todo_dao.get_todo_list_by_date(date)
        routine_list = self.routine_repository.get_routine_by_date(date)
        habit_list = self.habit_repository.get_habits_with_log_by_date(date)

        return TaskPublic(
            todo_list=todo_list,
            routine_list=routine_list,
            habit_list=habit_list,
        )
