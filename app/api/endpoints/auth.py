from fastapi import APIRouter, Depends, status

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


@router.post("/signup", response_model=Response[SignupOutput], status_code=201)
async def signup(
    data: SignupInput,
    auth_dao: AuthDAO = Depends(get_auth_dao),
    tx_manager: None = Depends(tx_manager),
):
    with tx_manager:
        user = auth_dao.sign_up(data)

    return Response(
        message="Signup success",
        status_code=status.HTTP_201_CREATED,
        data=SignupOutput.from_orm(user),
    )


@router.post("/login", response_model=Response[LoginOutput], status_code=200)
async def login(
    data: LoginInput,
    auth_dao: AuthDAO = Depends(get_auth_dao),
    tx_manager: None = Depends(tx_manager),
):
    with tx_manager:
        login_output = auth_dao.login(data.username, data.password)

    return Response(
        status_code=status.HTTP_200_OK,
        data=login_output,
    )


@router.post(
    "/refresh", response_model=Response[RefreshOutput], status_code=200
)
async def refresh(
    data: RefreshInput, auth_dao: AuthDAO = Depends(get_auth_dao)
):
    access_token = auth_dao.refresh(data.refresh_token)

    return Response(
        status_code=status.HTTP_200_OK,
        data=RefreshOutput(access_token=access_token),
    )
