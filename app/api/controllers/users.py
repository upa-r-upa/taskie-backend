from contextlib import contextmanager
from fastapi import APIRouter, Depends, status

from app.core.auth import verify_access_token

from ..dao import get_user_dao
from ..dao.user_dao import UserDAO
from app.database.db import tx_manager

from app.schemas.user import UserData, UserUpdateInput

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_access_token)],
)


@router.get(
    "/me",
    response_model=UserData,
    status_code=status.HTTP_200_OK,
    operation_id="getMe",
)
def get_me(
    user_dao: UserDAO = Depends(get_user_dao)
):
    return UserData.from_orm(user_dao.get_me())


@router.put(
    "/me",
    response_model=UserData,
    status_code=status.HTTP_200_OK,
    operation_id="updateMe",
)
def update_me(
    data: UserUpdateInput,
    user_dao: UserDAO = Depends(get_user_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        user = user_dao.update_me(data)

    return UserData.from_orm(user)
