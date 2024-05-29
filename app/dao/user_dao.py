from fastapi import HTTPException, status
from werkzeug.security import check_password_hash

from app.api.strings import (
    INVALID_LOGIN_ERROR,
    USERNAME_CANNOT_BE_CHANGED_ERROR,
)
from app.models.models import User
from app.schemas.user import UserUpdateInput

from .base import ProtectedBaseDAO


class UserDAO(ProtectedBaseDAO):
    def update_me(self, data: UserUpdateInput) -> User:
        user = self.db.query(User).filter_by(id=self.user_id).first()

        if data.username != self.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=USERNAME_CANNOT_BE_CHANGED_ERROR,
            )

        if not check_password_hash(user.password, data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_LOGIN_ERROR,
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
