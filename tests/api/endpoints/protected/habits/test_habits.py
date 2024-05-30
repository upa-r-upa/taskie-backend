from fastapi.testclient import TestClient
from pytest import Session

from app.models.models import Habit
from app.schemas.habit import HabitCreateInput, HabitDetail


def test_create_habit(
    client: TestClient,
    session: Session,
    habit_data: HabitCreateInput,
    access_token_headers: dict[str, str],
):
    response = client.post(
        "/habits/",
        json=habit_data.dict(),
        headers=access_token_headers,
    )

    response_data = HabitDetail(**response.json().get("data"))

    assert response.status_code == 201

    assert response_data.title == habit_data.title
    assert response_data.start_time_minutes == habit_data.start_time_minutes
    assert response_data.repeat_time_minutes == habit_data.repeat_time_minutes
    assert response_data.repeat_days == habit_data.repeat_days

    assert session.query(Habit).filter(Habit.id == response_data.id).first()
