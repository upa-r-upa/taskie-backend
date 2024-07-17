import pytest

from app.core.auth import create_refresh_token
from app.models.models import User


@pytest.fixture
def refresh_token(user_data: User) -> str:
    return create_refresh_token(user_data.username)
