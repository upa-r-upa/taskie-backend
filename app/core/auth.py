from functools import wraps
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Callable, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.strings import (
    USER_EXPIRED_AUTHENTICATED_ERROR,
    USER_NOT_AUTHENTICATED_ERROR,
)
from app.core.utils import get_user_by_username
from app.database import db

from app.models.models import User

from .config import JWT_SECRET_KEY, JWT_ALGORITHM


def generate_token(
    username: str, expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    payload = {"username": username, "exp": expire}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("username")
        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_EXPIRED_AUTHENTICATED_ERROR,
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (jwt.InvalidTokenError, jwt.DecodeError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=USER_NOT_AUTHENTICATED_ERROR,
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_access_token(username: str) -> str:
    expires_delta = timedelta(hours=6)  # 액세스 토큰의 만료 시간 설정
    return generate_token(username, expires_delta)


def generate_refresh_token(username: str) -> str:
    expires_delta = timedelta(days=30)  # 리프레시 토큰의 만료 시간 설정
    return generate_token(username, expires_delta)


security_scheme = HTTPBearer()


def get_current_user(
    db: Session = Depends(db.get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> User:
    token = credentials.credentials
    username = decode_token(token)

    user = get_user_by_username(db, username)

    return user


def jwt_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(
        current_user: User = Depends(get_current_user), *args, **kwargs
    ):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_AUTHENTICATED_ERROR,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*args, **kwargs)

    return wrapper
