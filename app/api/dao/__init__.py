from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.auth import verify_access_token

from app.database.db import get_db
from .routine_dao import RoutineDAO
from .routine_element_dao import RoutineElementDAO
from .todo_dao import TodoDAO
from .auth_dao import AuthDAO
from .user_dao import UserDAO
from .routine_log_dao import RoutineLogDAO


def get_routine_dao(
    db: Session = Depends(get_db),
    id: int = Depends(verify_access_token),
) -> RoutineDAO:
    return RoutineDAO(db=db, user_id=id)


def get_routine_item_dao(
    db: Session = Depends(get_db), id: int = Depends(verify_access_token)
) -> RoutineElementDAO:
    return RoutineElementDAO(db=db, user_id=id)


def get_todo_dao(
    db: Session = Depends(get_db), id: int = Depends(verify_access_token)
) -> TodoDAO:
    return TodoDAO(db=db, user_id=id)


def get_auth_dao(
    session: Session = Depends(get_db),
) -> AuthDAO:
    return AuthDAO(db=session)


def get_user_dao(
    session: Session = Depends(get_db), id: int = Depends(verify_access_token)
) -> UserDAO:
    return UserDAO(db=session, user_id=id)


def get_routine_log_dao(
    session: Session = Depends(get_db), id: int = Depends(verify_access_token)
) -> RoutineLogDAO:
    return RoutineLogDAO(db=session, user_id=id)
