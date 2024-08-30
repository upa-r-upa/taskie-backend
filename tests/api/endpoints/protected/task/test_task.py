from datetime import datetime
from fastapi.testclient import TestClient

from app.models.models import Todo
from app.schemas.habit import HabitWithLog
from app.schemas.routine import RoutinePublic


def test_get_all_daily_task_no_match_log(
    client: TestClient,
    access_token_headers: dict[str, str],
    add_todo_list: list[Todo],
    add_habit_list_with_log: list[HabitWithLog],
    add_routine_list_with_log: list[RoutinePublic],
):
    params = dict(date="2024-07-30")

    response = client.get(
        "/task",
        params=params,
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json().get("data")
    routine_list = response_data.get("routine_list")
    todo_list = response_data.get("todo_list")
    habit_list = response_data.get("habit_list")

    assert todo_list == []
    assert len(habit_list) == 3
    assert len(routine_list) == 3

    assert len(routine_list[0].get("routine_elements")) == 4


def test_get_all_daily_task(
    client: TestClient,
    access_token_headers: dict[str, str],
    add_todo_list: list[Todo],
    add_habit_list_with_log: list[HabitWithLog],
    add_routine_list_with_log: list[RoutinePublic],
    target_date: datetime,
):
    params = dict(date=target_date.strftime("%Y-%m-%d"))

    response = client.get(
        "/task",
        params=params,
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json().get("data")
    routine_list = response_data.get("routine_list")
    todo_list = response_data.get("todo_list")
    habit_list = response_data.get("habit_list")

    assert len(todo_list) == 4
    assert (
        datetime.strptime(
            todo_list[0].get("target_date"), "%Y-%m-%dT%H:%M:%S"
        ).date()
        == target_date.date()
    )
    assert len(habit_list) == 2
    assert target_date.weekday() in habit_list[0].get("repeat_days")

    assert habit_list[0].get("id") == 4
    assert habit_list[1].get("id") == 3

    assert len(habit_list[0].get("log_list")) == 5
    assert len(habit_list[1].get("log_list")) == 4

    assert len(routine_list) == 3
    assert len(routine_list[0].get("routine_elements")) == 4
    assert (
        routine_list[0].get("routine_elements")[0].get("completed_at")
        is not None
    )
