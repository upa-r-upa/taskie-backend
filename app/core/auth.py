from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from pytz import timezone
from pydantic import BaseModel
from typing import Annotated, Literal
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from app.api.errors import EXPIRED_TOKEN, INVALID_CREDENTIAL
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
    id: int | None = None
    type: Annotated[Literal["refresh", "access"], None] = None


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone("Asia/Seoul")) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(id: int):
    return create_jwt_token(
        data=TokenData(id=id, type="refresh").dict(),
        expires_delta=JWT_REFRESH_TOKEN_EXPIRES,
    )


def create_access_token(id: int):
    return create_jwt_token(
        data=TokenData(id=id, type="access").dict(),
        expires_delta=JWT_ACCESS_TOKEN_EXPIRES,
    )


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=INVALID_CREDENTIAL,
    headers={"WWW-Authenticate": "Bearer"},
)


def refresh_token_decode(refresh_token: str) -> User:
    try:
        payload = jwt.decode(
            refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        id: int | None = payload.get("id")
        type: str | None = payload.get("type")

        if id is None or type != "refresh":
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    return id


def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> int:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        id: int | None = payload.get("id")
        type: str | None = payload.get("type")

        if id is None or type != "access":
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=EXPIRED_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception

    return id
