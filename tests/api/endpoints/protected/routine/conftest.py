import pytest

from app.schemas.routine import RoutineCreateInput


@pytest.fixture
def routine() -> RoutineCreateInput:
    return RoutineCreateInput(
        title="아침 루틴",
        start_time_minutes=480,
        repeat_days=[1, 2, 3, 4, 5],
        todo_items=[
            {"title": "스트레칭 하기", "duration_minutes": 10},
            {"title": "물 마시기", "duration_minutes": 5},
            {"title": "이불 개기", "duration_minutes": 3},
        ],
    )
