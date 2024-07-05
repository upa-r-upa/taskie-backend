from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from pytest import Session
from app.api.strings import USER_NOT_AUTHENTICATED_ERROR
from app.models.models import User


def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_AUTHENTICATED_ERROR,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def validate_date_format(date_str: Optional[str]) -> Optional[datetime]:
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                detail=f"Invalid date format: {date_str}. Required format YYYY-MM-DD.",
            )
    return None
