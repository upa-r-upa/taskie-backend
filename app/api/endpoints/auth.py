from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.auth import decode_token, generate_access_token, generate_refresh_token
from app.database.db import get_db
from app.models.models import User
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


def user_exists(db: Session, username: str, email: str):
    if db.query(User).filter_by(username=username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )


@router.post("/signup", response_model=Response[SignupOutput], status_code=201)
async def signup(data: SignupInput, db: Session = Depends(get_db)):
    password_hash = generate_password_hash(data.password)

    user = User(
        username=data.username,
        password=password_hash,
        email=data.email,
        grade=data.grade,
        profile_image=data.profile_image,
        nickname=data.nickname or data.username,
    )

    user_exists(db, user.username, user.email)

    try:
        db.add(user)
        db.commit()

        return Response(
            message="Signup success",
            status_code=status.HTTP_201_CREATED,
            data=SignupOutput.from_orm(user),
        )
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred",
        )


@router.post("/login", response_model=Response[LoginOutput], status_code=200)
async def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is wrong",
        )

    if not check_password_hash(user.password, data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is wrong",
        )

    access_token = generate_access_token(user.username)
    refresh_token = generate_refresh_token(user.username)

    return Response(
        message="Login success",
        status_code=status.HTTP_200_OK,
        data=LoginOutput(access_token=access_token, refresh_token=refresh_token),
    )


@router.post("/refresh", response_model=Response[RefreshOutput], status_code=200)
async def refresh(data: RefreshInput, db: Session = Depends(get_db)):
    if not data.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required",
        )

    username = decode_token(data.refresh_token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = generate_access_token(username)

    return Response(
        message="Access token refreshed",
        status_code=status.HTTP_200_OK,
        data=RefreshOutput(access_token=access_token),
    )
