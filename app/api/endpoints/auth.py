from fastapi import APIRouter, Depends, status, Response as FastAPIResponse

from app.dao import get_auth_dao
from app.dao.auth_dao import AuthDAO
from app.database.db import tx_manager
from app.schemas.response import Response
from app.schemas.auth import (
    LoginInput,
    LoginOutput,
    RefreshInput,
    RefreshOutput,
    SignupInput,
    SignupOutput,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=Response[SignupOutput],
    status_code=status.HTTP_201_CREATED,
    operation_id="signup",
)
def signup(
    data: SignupInput,
    auth_dao: AuthDAO = Depends(get_auth_dao),
    tx_manager: None = Depends(tx_manager),
):
    with tx_manager:
        user = auth_dao.sign_up(data)

    return Response(
        message="Signup success",
        data=SignupOutput.from_orm(user),
    )


@router.post(
    "/login",
    response_model=Response[LoginOutput],
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
        refresh_token, access_token = auth_dao.login(
            data.username, data.password
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 7,
            secure=True,
            samesite="strict",
        )

    return Response(
        data=LoginOutput(access_token=access_token),
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
    response.delete_cookie(key="refresh_token")

    return None


@router.post(
    "/refresh",
    response_model=Response[RefreshOutput],
    status_code=status.HTTP_200_OK,
    operation_id="refreshToken",
)
async def refresh(
    data: RefreshInput, auth_dao: AuthDAO = Depends(get_auth_dao)
):
    access_token = auth_dao.refresh(data.refresh_token)

    return Response(
        data=RefreshOutput(access_token=access_token),
    )
