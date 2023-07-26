from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User

from app.schemas.auth import SignupInput, SignupOutput


def test_signup(client: TestClient, session: Session):
    data = SignupInput(
        username="test",
        password="test123",
        password_confirm="test123",
        email="test@test.com",
        grade=1,
        profile_image="test",
        nickname="test",
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
