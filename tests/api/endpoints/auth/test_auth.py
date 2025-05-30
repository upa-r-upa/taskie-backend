from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User

from app.schemas.auth import (
    SignupInput,
    UserBase,
)


def test_signup(client: TestClient, session: Session, user_data: UserBase):
    data = SignupInput(
        username=user_data.username,
        password=user_data.password,
        password_confirm=user_data.password,
        email=user_data.email,
        nickname=user_data.nickname,
    )

    response = client.post("/auth/signup", json=data.dict())

    assert response.status_code == 201

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == data.username
    assert user.email == data.email
    assert user.nickname == data.nickname


def test_signup_starting_with_number(client: TestClient, session: Session):
    data = SignupInput(
        username="123user",
        password="123P@ss!",
        password_confirm="123P@ss!",
        email="number.start@example.com",
        nickname="123닉네임",
    )

    response = client.post("/auth/signup", json=data.dict())

    assert response.status_code == 201

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == data.username
    assert user.email == data.email
    assert user.nickname == data.nickname


def test_signup_with_special_password(client: TestClient, session: Session):
    data = SignupInput(
        username="testuser",
        password="P@ssw0rd!",
        password_confirm="P@ssw0rd!",
        email="special.chars@example.com",
        nickname="닉네임_!@#$%",
    )

    response = client.post("/auth/signup", json=data.dict())

    assert response.status_code == 201

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == data.username
    assert user.email == data.email
    assert user.nickname == data.nickname


def test_signup_with_special_character_in_username_fails(client: TestClient):
    data = dict(
        username="test!user",
        password="password123",
        password_confirm="password123",
        email="test.special@example.com",
        nickname="테스트유저",
    )

    response = client.post("/auth/signup", json=data)

    assert response.status_code == 422


def test_login(client: TestClient, user_data: UserBase, add_user: User):
    data = dict(
        username=add_user.username,
        password=user_data.password,
    )

    response = client.post("/auth/login", json=data)
    response_json_user = response.json().get("user")

    assert response.status_code == 200

    assert response.cookies.get("refresh_token") is not None
    assert response.json().get("access_token")

    assert response_json_user.get("username") == user_data.username
    assert response_json_user.get("email") == user_data.email
    assert response_json_user.get("nickname") == user_data.nickname


def test_login_invalid_data(
    client: TestClient, user_data: UserBase, add_user: User
):
    data = dict(username="invalid_username", password="invalid_password")

    response = client.post("/auth/login", json=data)

    assert response.status_code == 401


def test_logout(client: TestClient, add_user: User):
    response = client.post("/auth/logout")

    assert response.status_code == 204
    assert response.cookies.get("refresh_token") is None


def test_refresh(
    client: TestClient, refresh_token: str, user_data: UserBase
):
    response = client.post(
        "/auth/refresh", cookies={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    assert response.json().get("access_token")


def test_refresh_with_user_info(
    client: TestClient, refresh_token: str, user_data: UserBase, add_user: User
):
    response = client.post(
        "/auth/refresh?include_user_info=true", 
        cookies={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    response_json = response.json()
    
    # 토큰 확인
    assert response_json.get("access_token")
    
    # 사용자 정보 확인
    assert response_json.get("user") is not None
    user_info = response_json.get("user")
    assert user_info.get("username") == add_user.username
    assert user_info.get("email") == add_user.email
    assert user_info.get("nickname") == add_user.nickname


def test_refresh_without_user_info(
    client: TestClient, refresh_token: str
):
    response = client.post(
        "/auth/refresh", 
        cookies={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    response_json = response.json()
    
    # 토큰 확인
    assert response_json.get("access_token")
    
    # 사용자 정보 없음 확인
    assert response_json.get("user") is None


def test_invalid_refresh(
    client: TestClient, refresh_token: str
):
    response = client.post("/auth/refresh", cookies={"refresh_token": "test"})

    assert response.status_code == 401
    assert response.cookies.get("refresh_token") is None


def test_null_refresh(client: TestClient):
    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.cookies.get("refresh_token") is None
