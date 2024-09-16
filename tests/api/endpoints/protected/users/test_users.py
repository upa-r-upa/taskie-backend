from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.auth import UserBase

from app.schemas.user import UserData, UserUpdateInput


def test_get_me(
    client: TestClient,
    access_token_headers: dict[str, str],
    user_data: UserBase,
):
    excepted_output = UserData.from_orm(user_data)

    response = client.get("/users/me", headers=access_token_headers)

    assert response.status_code == 200
    assert response.json() == excepted_output.dict()


def test_update_me(
    client: TestClient,
    session: Session,
    access_token_headers: dict[str, str],
    user_data: UserBase,
):
    excepted_output = UserData.from_orm(user_data)

    excepted_output.nickname = "test_nickname"
    excepted_output.email = "test@test.com2"

    data = UserUpdateInput(
        username=excepted_output.username,
        password=user_data.password,
        email=excepted_output.email,
        nickname=excepted_output.nickname,
    )

    response = client.put(
        "/users/me",
        headers=access_token_headers,
        json=data.dict(),
    )

    assert response.status_code == 200
    assert response.json() == excepted_output.dict()

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == excepted_output.username
    assert user.email == excepted_output.email
    assert user.nickname == excepted_output.nickname
