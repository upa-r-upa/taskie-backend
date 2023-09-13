from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.db import get_db
from .routine_repository import RoutineRepository


def get_routine_repository(
    db: Session = Depends(get_db), user: int = Depends(get_current_user)
):
    return RoutineRepository(db=db, user_id=user.id)
