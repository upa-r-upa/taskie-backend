from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response as FastAPIResponse,
    Cookie,
)

from ..dao import get_auth_dao
from ..dao.auth_dao import AuthDAO
from app.database.db import tx_manager

from app.schemas.auth import (
    LoginInput,
    LoginOutput,
    RefreshOutput,
    SignupInput,
)
from app.schemas.user import UserData

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    operation_id="signup",
)
def signup(
    data: SignupInput,
    auth_dao: AuthDAO = Depends(get_auth_dao),
    tx_manager: None = Depends(tx_manager),
):
    with tx_manager:
        auth_dao.sign_up(data)

    return None


@router.post(
    "/login",
    response_model=LoginOutput,
    status_code=status.HTTP_200_OK,
    operation_id="login",
)
def login(
    data: LoginInput,
    response: FastAPIResponse,
    auth_dao: AuthDAO = Depends(get_auth_dao),
    tx_manager: None = Depends(tx_manager),
):
    with tx_manager:
        refresh_token, access_token, user = auth_dao.login(
            data.username, data.password
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 7,
            secure=True,
            samesite="lax",
        )

    return LoginOutput(
        access_token=access_token,
        user=UserData.from_orm(user),
    )


@router.post(
    "/logout",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="logout",
)
def logout(
    response: FastAPIResponse,
):
    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        max_age=0,
        secure=True,
        samesite="lax",
    )

    return None


@router.post(
    "/refresh",
    response_model=RefreshOutput,
    status_code=status.HTTP_200_OK,
    operation_id="refreshToken",
)
async def refresh(
    response: FastAPIResponse,
    include_user_info: bool = False,
    refresh_token: Annotated[str | None, Cookie()] = None,
    auth_dao: AuthDAO = Depends(get_auth_dao),
):
    if not refresh_token:
        headers = {
            "WWW-Authenticate": 'Bearer realm="Access to the refresh API", \
            error="invalid_token",\
            error_description="The refresh token is missing"'
        }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers=headers,
        )

    try:
        if include_user_info:
            access_token, user = auth_dao.refresh_with_user_info(
                refresh_token=refresh_token
            )
            return RefreshOutput(
                access_token=access_token,
                user=UserData.from_orm(user)
            )
        else:
            access_token = auth_dao.refresh(refresh_token=refresh_token)
            return RefreshOutput(access_token=access_token)
    except HTTPException as e:
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            max_age=0,
            secure=True,
            samesite="lax",
        )
        raise e
