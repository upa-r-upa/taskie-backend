from functools import wraps
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from typing import Callable, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import JWT_SECRET_KEY, JWT_ALGORITHM


def generate_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
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
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (jwt.DecodeError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
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
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    token = credentials.credentials
    username = decode_token(token)

    return username


def jwt_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(current_user: str = Depends(get_current_user), *args, **kwargs):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*args, **kwargs)

    return wrapper
