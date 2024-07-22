from fastapi import HTTPException, status

from app.api.errors import (
    INCORRECT_USERNAME_OR_PASSWORD,
    USERNAME_CANNOT_BE_CHANGED,
)
from app.core.auth import verify_password
from app.models.models import User
from app.schemas.user import UserUpdateInput

from .base import ProtectedBaseDAO


class UserDAO(ProtectedBaseDAO):
    def update_me(self, data: UserUpdateInput) -> User:
        user = self.db.query(User).filter_by(id=self.user_id).first()

        if data.username != self.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=USERNAME_CANNOT_BE_CHANGED,
            )

        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INCORRECT_USERNAME_OR_PASSWORD,
            )

        if data.email:
            user.email = data.email

        if data.profile_image == "":
            user.profile_image = None
        elif data.profile_image:
            user.profile_image = data.profile_image

        if data.nickname:
            user.nickname = data.nickname

        return user
