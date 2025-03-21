import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from passlib.context import CryptContext


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import DATABASE_URI
from app.schemas.auth import UserBase
from app.database.db import Base, get_db
from app.models.models import User
from app.core.auth import create_access_token
from app.main import app as client_app

engine = create_engine(DATABASE_URI, echo=True)
TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(autouse=True)
def app():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield client_app

    Base.metadata.drop_all(engine)


@pytest.fixture
def session(app: FastAPI):
    session = TestingSessionLocal()

    yield session

    session.close()


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
def user_data() -> UserBase:
    user = UserBase(
        username="test",
        password="test123",
        email="test@test.com",
        nickname="test",
    )

    return user


@pytest.fixture
def add_user(session: Session, user_data: UserBase) -> User:
    user = User(
        username=user_data.username,
        password=pwd_context.hash(user_data.password),
        email=user_data.email,
        nickname=user_data.nickname,
    )

    session.add(user)
    session.commit()

    return user


@pytest.fixture
def access_token(add_user: User) -> str:
    return create_access_token(add_user.id)


@pytest.fixture
def access_token_headers(access_token: str) -> dict[str, str]:
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
