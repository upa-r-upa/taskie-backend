from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from app.core.auth import get_current_user
from app.core.utils import get_user_by_username
from app.database.db import get_db
from app.schemas.response import Response
from app.schemas.user import UserData, UserUpdateInput

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/me", response_model=Response[UserData], status_code=status.HTTP_200_OK)
def get_me(db: Session = Depends(get_db), username=Depends(get_current_user)):
    user = get_user_by_username(db, username)

    return Response(
        status_code=status.HTTP_200_OK,
        data=UserData.from_orm(user),
        message="User data retrieved successfully",
    )


@router.put("/me", response_model=Response[UserData], status_code=status.HTTP_200_OK)
def update_me(
    data: UserUpdateInput,
    db: Session = Depends(get_db),
    username=Depends(get_current_user),
):
    user = get_user_by_username(db, username)

    if data.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Username cannot be changed"
        )

    if check_password_hash(user.password, data.password) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is wrong"
        )

    if data.email:
        user.email = data.email

    if data.grade:
        user.grade = data.grade

    if data.profile_image == "":
        user.profile_image = None
    elif data.profile_image:
        user.profile_image = data.profile_image

    if data.nickname:
        user.nickname = data.nickname

    try:
        db.commit()

        return Response(
            status_code=status.HTTP_200_OK,
            data=UserData.from_orm(user),
            message="User data updated successfully",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User data update failed",
        )
