from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated, Literal
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.db import get_db
from app.models.models import User

from .config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()


class TokenData(BaseModel):
    username: str | None = None
    type: Annotated[Literal["refresh", "access"], None] = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(username: str):
    return create_jwt_token(
        data=TokenData(username=username, type="refresh").dict(),
        expires_delta=JWT_REFRESH_TOKEN_EXPIRES,
    )


def create_access_token(username: str):
    return create_jwt_token(
        data=TokenData(username=username, type="access").dict(),
        expires_delta=JWT_ACCESS_TOKEN_EXPIRES,
    )


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user(db: Session, username: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()

    return user


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def refresh_token_decode(refresh_token: str, db: Session) -> User:
    try:
        payload = jwt.decode(
            refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        username: str | None = payload.get("username")
        type: str | None = payload.get("type")

        if username is None or type != "refresh":
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=username)

    if user is None:
        raise credentials_exception

    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str | None = payload.get("username")
        type: str | None = payload.get("type")

        if username is None or type != "access":
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db=db, username=username)

    if user is None:
        raise credentials_exception

    return user
