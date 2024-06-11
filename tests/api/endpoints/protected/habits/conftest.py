import pytest

from app.schemas.habit import HabitCreateInput


@pytest.fixture
def habit_data() -> HabitCreateInput:
    return HabitCreateInput(
        title="물 마시기",
        start_time_minutes=480,
        end_time_minutes=1380,
        repeat_time_minutes=30,
        repeat_days=[1, 2, 3, 4, 5, 6, 7],
    )
