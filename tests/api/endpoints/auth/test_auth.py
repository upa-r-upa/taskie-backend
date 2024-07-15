from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User

from app.schemas.auth import (
    LoginInput,
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

    assert response.cookies.get("refresh_token") is not None
    assert response.json().get("data").get("access_token")


def test_logout(client: TestClient, add_user: User):
    response = client.post("/auth/logout")

    assert response.status_code == 204
    assert response.cookies.get("refresh_token") is None


def test_refresh(client: TestClient, refresh_token: str):
    response = client.post(
        "/auth/refresh", cookies={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    assert response.json().get("data").get("access_token")


def test_invalid_refresh(client: TestClient, refresh_token: str):
    response = client.post("/auth/refresh", cookies={"refresh_token": "test"})

    assert response.status_code == 401
    assert response.cookies.get("refresh_token") is None


def test_null_refresh(client: TestClient):
    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.cookies.get("refresh_token") is None
