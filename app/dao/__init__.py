from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user

from app.database.db import get_db

from .routine_dao import RoutineDAO
from .routine_element_dao import RoutineElementDAO


def get_routine_dao(
    db: Session = Depends(get_db), user: int = Depends(get_current_user)
):
    return RoutineDAO(db=db, user_id=user.id)


def get_routine_item_dao(
    db: Session = Depends(get_db), user: int = Depends(get_current_user)
):
    return RoutineElementDAO(db=db, user_id=user.id)
