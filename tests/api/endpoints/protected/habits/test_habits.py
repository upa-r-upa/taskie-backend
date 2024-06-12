from datetime import datetime
from typing import List
from fastapi.testclient import TestClient
from pytest import Session

from app.models.models import Habit, HabitLog
from app.schemas.habit import (
    HabitCreateInput,
    HabitDetail,
    HabitListGetInput,
    HabitWithLog,
)


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
    assert response_data.end_time_minutes == habit_data.end_time_minutes
    assert response_data.repeat_time_minutes == habit_data.repeat_time_minutes
    assert response_data.repeat_days == habit_data.repeat_days

    assert session.query(Habit).filter(Habit.id == response_data.id).first()


def test_get_habits(
    client: TestClient,
    session: Session,
    add_habit_list: list[Habit],
    add_habit_log_list: list[HabitLog],
    access_token_headers: dict[str, str],
):
    response = client.get(
        "/habits/",
        headers=access_token_headers,
        params=HabitListGetInput(
            limit=3,
            log_target_date=datetime(2024, 6, 13),
        ).dict(),
    )

    response_data: List[HabitWithLog] = [
        HabitWithLog(**habit) for habit in response.json().get("data")
    ]

    assert response.status_code == 200

    assert len(response_data) == 3
    assert response_data[2].id == add_habit_list[0].id
    assert response_data[1].id == add_habit_list[1].id
    assert response_data[0].id == add_habit_list[2].id

    assert len(response_data[0].log_list) == 5
    assert len(response_data[1].log_list) == 5
    assert len(response_data[2].log_list) == 0

    assert response_data[0].log_list[0].id == add_habit_log_list[0].id
    assert response_data[1].log_list[0].id == add_habit_log_list[5].id
