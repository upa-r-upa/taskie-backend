from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.strings import (
    EMAIL_ALREADY_EXISTS_ERROR,
    INVALID_LOGIN_ERROR,
    REQUIRE_REFRESH_TOKEN_ERROR,
    USER_NOT_AUTHENTICATED_ERROR,
    USERNAME_ALREADY_EXISTS_ERROR,
)
from app.core.auth import (
    decode_token,
    generate_access_token,
    generate_refresh_token,
)

from app.models.models import User
from app.schemas.auth import LoginOutput, SignupInput

from .base import BaseDAO


class AuthDAO(BaseDAO):
    def check_existing_email(self, email: str) -> bool:
        return self.db.query(User).filter_by(email=email).first() is not None

    def check_existing_username(self, username: str) -> bool:
        return (
            self.db.query(User).filter_by(username=username).first()
            is not None
        )

    def sign_up(self, data: SignupInput) -> User:
        password_hash = generate_password_hash(data.password)

        user = User(
            username=data.username,
            password=password_hash,
            email=data.email,
            grade=data.grade,
            profile_image=data.profile_image,
            nickname=data.nickname or data.username,
        )

        if self.check_existing_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=USERNAME_ALREADY_EXISTS_ERROR,
            )

        if self.check_existing_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=EMAIL_ALREADY_EXISTS_ERROR,
            )

        self.db.add(user)

        return user

    def login(self, username: str, password: str) -> LoginOutput:
        user = self.db.query(User).filter_by(username=username).first()
        # SELECT * FROM user WHERE username = :username

        if not user or not check_password_hash(user.password, password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_LOGIN_ERROR,
            )

        access_token = generate_access_token(user.username)
        refresh_token = generate_refresh_token(user.username)

        return LoginOutput(
            access_token=access_token, refresh_token=refresh_token
        )

    def refresh(self, refresh_token: str) -> str:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=REQUIRE_REFRESH_TOKEN_ERROR,
            )

        username = decode_token(refresh_token)

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_AUTHENTICATED_ERROR,
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = generate_access_token(username)

        return access_token
