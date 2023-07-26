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


def test_signup(client: TestClient, session: Session, test_user_data: UserBase):
    data = SignupInput(
        username=test_user_data.username,
        password=test_user_data.password,
        password_confirm=test_user_data.password,
        email=test_user_data.email,
        grade=test_user_data.grade,
        profile_image=test_user_data.profile_image,
        nickname=test_user_data.nickname,
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


def test_login(client: TestClient, test_user_data: UserBase, create_test_user: User):
    data = LoginInput(
        username=create_test_user.username,
        password=test_user_data.password,
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
