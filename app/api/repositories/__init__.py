from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth import verify_access_token
from app.database.db import get_db
from .habit_repository import HabitRepository
from .task_repository import TaskRepository
from .routine_repository import RoutineRepository


def get_routine_repository(
    db: Session = Depends(get_db), id: int = Depends(verify_access_token)
):
    return RoutineRepository(db=db, user_id=id)


def get_habit_repository(
    db: Session = Depends(get_db), id: int = Depends(verify_access_token)
):
    return HabitRepository(db=db, user_id=id)


def get_task_repository(
    db: Session = Depends(get_db), id: int = Depends(verify_access_token)
):
    return TaskRepository(db=db, user_id=id)
