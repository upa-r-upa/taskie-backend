from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.auth import UserBase

from app.schemas.user import UserData, UserUpdateInput


def test_get_me(
    client: TestClient,
    access_token: str,
    create_test_user: User,
):
    excepted_output = UserData.from_orm(create_test_user)

    response = client.get(
        "/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json().get("data") == excepted_output.dict()


def test_update_me(
    client: TestClient,
    session: Session,
    access_token: str,
    test_user_data: UserBase,
    create_test_user: User,
):
    excepted_output = UserData.from_orm(create_test_user)

    excepted_output.nickname = "test_nickname"
    excepted_output.email = "test@test.com2"
    excepted_output.profile_image = "test2"

    data = UserUpdateInput(
        username=excepted_output.username,
        password=test_user_data.password,
        email=excepted_output.email,
        profile_image=excepted_output.profile_image,
        nickname=excepted_output.nickname,
    )

    response = client.put(
        "/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json=data.dict(),
    )

    assert response.status_code == 200
    assert response.json().get("data") == excepted_output.dict()

    user = session.query(User).filter_by(username=data.username).first()

    assert user.username == excepted_output.username
    assert user.email == excepted_output.email
    assert user.profile_image == excepted_output.profile_image
    assert user.nickname == excepted_output.nickname
