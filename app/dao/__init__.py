from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user

from app.database.db import get_db
from app.models.models import User
from .routine_dao import RoutineDAO
from .routine_element_dao import RoutineElementDAO
from .todo_dao import TodoDAO
from .auth_dao import AuthDAO
from .user_dao import UserDAO


def get_routine_dao(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RoutineDAO:
    return RoutineDAO(db=db, user=user)


def get_routine_item_dao(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> RoutineElementDAO:
    return RoutineElementDAO(db=db, user=user)


def get_todo_dao(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> TodoDAO:
    return TodoDAO(db=db, user=user)


def get_auth_dao(
    session: Session = Depends(get_db),
) -> AuthDAO:
    return AuthDAO(db=session)


def get_user_dao(
    session: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> UserDAO:
    return UserDAO(db=session, user=user)
