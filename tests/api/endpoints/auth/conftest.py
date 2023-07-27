import pytest

from app.core.auth import generate_refresh_token
from app.models.models import User


@pytest.fixture
def refresh_token(user_data: User) -> str:
    return generate_refresh_token(user_data.username)
