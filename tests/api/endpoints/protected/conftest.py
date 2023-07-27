import pytest
from app.models.models import User


@pytest.fixture(autouse=True)
def login_mock(add_user: User):
    yield add_user
