from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User

from app.schemas.auth import (
    LoginInput,
    RefreshInput,
    SignupInput,
    SignupOutput,
    UserBase,
)


def test_signup(client: TestClient, session: Session, user_data: UserBase):
    data = SignupInput(
        username=user_data.username,
        password=user_data.password,
        password_confirm=user_data.password,
        email=user_data.email,
        grade=user_data.grade,
        profile_image=user_data.profile_image,
        nickname=user_data.nickname,
    )

    expected_output = SignupOutput(
        username=data.username,
        email=data.email,
        grade=data.grade,
        profile_image=data.profile_image,
        nickname=data.nickname,
    )

    response = client.post("/auth/signup", json=data.dict())

    assert response.status_code == 201
    assert response.json().get("data") == expected_output.dict()

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == data.username
    assert user.email == data.email
    assert user.grade == data.grade
    assert user.profile_image == data.profile_image
    assert user.nickname == data.nickname


def test_login(client: TestClient, user_data: UserBase, add_user: User):
    data = LoginInput(
        username=add_user.username,
        password=user_data.password,
    )

    response = client.post("/auth/login", json=data.dict())

    assert response.status_code == 200
    assert response.json().get("data").get("access_token")
    assert response.json().get("data").get("refresh_token")


def test_refresh(client: TestClient, refresh_token: str):
    data = RefreshInput(refresh_token=refresh_token)

    response = client.post("/auth/refresh", json=data.dict())

    assert response.status_code == 200
    assert response.json().get("data").get("access_token")
