from typing import Tuple
from fastapi import HTTPException, status
from app.api.errors import (
    EMAIL_ALREADY_EXISTS,
    INCORRECT_USERNAME_OR_PASSWORD,
    USER_NOT_FOUND,
    USERNAME_ALREADY_EXISTS,
)
from app.core.auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    refresh_token_decode,
    verify_password,
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

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)

        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def get_user_by_username(self, username: str) -> User | None:
        user = self.db.query(User).filter(User.username == username).first()

        return user
    
    def get_user_by_id(self, id: int) -> User | None:
        user = self.db.query(User).filter(User.id == id).first()

        return user

    def login(self, username: str, password: str) -> Tuple[str, str, User]:
        user = self.authenticate_user(username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_USERNAME_OR_PASSWORD,
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return refresh_token, access_token, user

    def refresh(self, refresh_token: str) -> str:
        id: int = refresh_token_decode(refresh_token)
        access_token = create_access_token(id)

        return access_token

    def refresh_with_user_info(self, refresh_token: str) -> Tuple[str, User]:
        id: int = refresh_token_decode(refresh_token)
        access_token = create_access_token(id)
        
        user = self.get_user_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=USER_NOT_FOUND,
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return access_token, user
    