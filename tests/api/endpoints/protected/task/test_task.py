from datetime import datetime
from fastapi.testclient import TestClient

from app.models.models import Todo
from app.schemas.habit import HabitWithLog
from app.schemas.routine import RoutinePublic


def test_get_all_daily_task_empty(
    client: TestClient,
    access_token_headers: dict[str, str],
):
    params = dict(date="2024-07-30")

    response = client.get(
        "/task",
        params=params,
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json()
    routine_list = response_data.get("routine_list")
    todo_list = response_data.get("todo_list")
    habit_list = response_data.get("habit_list")

    assert todo_list == []
    assert routine_list == []
    assert habit_list == []


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

    response_data = response.json()
    routine_list = response_data.get("routine_list")
    todo_list = response_data.get("todo_list")
    habit_list = response_data.get("habit_list")

    assert len(todo_list) == 3
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

    response_data = response.json()
    routine_list = response_data.get("routine_list")
    todo_list = response_data.get("todo_list")
    habit_list = response_data.get("habit_list")

    assert len(todo_list) == 5

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


def test_get_uncompleted_todo_task(
    client: TestClient,
    access_token_headers: dict[str, str],
    previous_target_date: datetime,
    target_date: datetime,
    add_todo_list_with_previous_todo: list[Todo],
):
    params = dict(date=target_date.strftime("%Y-%m-%d"))

    response = client.get(
        "/task",
        params=params,
        headers=access_token_headers,
    )

    response_data = response.json()
    todo_list = response_data.get("todo_list")

    assert response.status_code == 200

    assert len(todo_list) == 6

    assert todo_list[0]["target_date"].startswith(
        target_date.strftime("%Y-%m-%d")
    )
    assert todo_list[0]["completed_at"] is None

    assert todo_list[2]["target_date"].startswith(
        previous_target_date.strftime("%Y-%m-%d")
    )
    assert todo_list[2]["completed_at"] is None
