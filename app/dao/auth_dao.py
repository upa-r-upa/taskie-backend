from typing import Tuple
from fastapi import HTTPException, status
from app.api.errors import (
    EMAIL_ALREADY_EXISTS,
    INCORRECT_USERNAME_OR_PASSWORD,
    USERNAME_ALREADY_EXISTS,
)
from app.core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    refresh_token_decode,
)

from app.models.models import User
from app.schemas.auth import SignupInput

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
        password_hash = get_password_hash(data.password)

        user = User(
            username=data.username,
            password=password_hash,
            email=data.email,
            nickname=data.nickname or data.username,
            grade=0,
            profile_image="",
        )

        if self.check_existing_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=USERNAME_ALREADY_EXISTS,
            )

        if self.check_existing_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=EMAIL_ALREADY_EXISTS,
            )

        self.db.add(user)

        return user

    def login(self, username: str, password: str) -> Tuple[str, str, User]:
        user = authenticate_user(self.db, username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_USERNAME_OR_PASSWORD,
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return refresh_token, access_token, user

    def refresh(self, refresh_token: str) -> Tuple[str, User]:
        user: User = refresh_token_decode(refresh_token, self.db)
        access_token = create_access_token(user.username)

        return access_token, user
