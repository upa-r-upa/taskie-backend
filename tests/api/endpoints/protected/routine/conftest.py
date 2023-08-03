import pytest

from app.schemas.routine import RoutineCreateInput, RoutineItemBase


@pytest.fixture
def routine() -> RoutineCreateInput:
    return RoutineCreateInput(
        title="아침 루틴",
        start_time_minutes=480,
        repeat_days=[1, 2, 3, 4, 5],
        routine_items=[
            RoutineItemBase(title="아침 물 마시기", duration_minutes=5, order=1),
            RoutineItemBase(title="아침 운동하기", duration_minutes=30, order=2),
            RoutineItemBase(title="아침 식사하기", duration_minutes=15, order=3),
        ],
    )
