from fastapi import HTTPException, status
from app.database.db import SessionLocal
from app.models.models import User


def get_user_by_username(db: SessionLocal, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
