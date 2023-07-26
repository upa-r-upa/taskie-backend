import os
import sys
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from werkzeug.security import generate_password_hash


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.schemas.auth import UserBase
from app.database.db import get_db
from app.models.models import User
from app.core.auth import generate_access_token, generate_refresh_token
from main import app as client_app

engine = create_engine(os.environ.get("TSK_SQLALCHEMY_URL"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@pytest.fixture(autouse=True)
def app():
    Base.metadata.create_all(engine)

    yield client_app

    Base.metadata.drop_all(engine)


@pytest.fixture
def session(app: FastAPI):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(app: FastAPI, session: Session):
    def get_db_override():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = get_db_override

    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user_data() -> UserBase:
    user = UserBase(
        username="test",
        password="test123",
        email="test@test.com",
        grade=1,
        profile_image="test",
        nickname="test",
    )

    return user


@pytest.fixture
def create_test_user(session: Session, test_user_data: UserBase) -> User:
    user = User(
        username=test_user_data.username,
        password=generate_password_hash(test_user_data.password),
        email=test_user_data.email,
        grade=test_user_data.grade,
        profile_image=test_user_data.profile_image,
        nickname=test_user_data.nickname,
    )

    session.add(user)
    session.commit()

    yield user


@pytest.fixture
def refresh_token(test_user_data: User) -> str:
    return generate_refresh_token(test_user_data.username)


@pytest.fixture
def access_token(test_user_data: UserBase) -> str:
    return generate_access_token(test_user_data.username)
