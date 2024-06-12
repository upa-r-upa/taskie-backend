from datetime import datetime
from typing import List
from pytest import Session, fixture

from app.models.models import Habit, HabitLog, User
from app.schemas.habit import HabitCreateInput


@fixture
def habit_data() -> HabitCreateInput:
    return HabitCreateInput(
        title="물 마시기",
        start_time_minutes=480,
        end_time_minutes=1380,
        repeat_time_minutes=30,
        repeat_days=[1, 2, 3, 4, 5, 6, 7],
    )


@fixture
def habit_list() -> List[Habit]:
    return [
        Habit(
            title="습관 1",
            start_time_minutes=480,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days=[1, 2, 3, 4, 5, 6, 7],
        ),
        Habit(
            title="습관 2",
            start_time_minutes=600,
            end_time_minutes=1380,
            repeat_time_minutes=60,
            repeat_days=[1, 2, 3, 4, 5],
        ),
        Habit(
            title="습관 3",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days=[1, 2, 3, 4, 5, 6, 7],
        ),
        Habit(
            title="습관 4",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days=[1, 2, 3, 4, 5, 6, 7],
        ),
        Habit(
            title="습관 5",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days=[1, 2, 3, 4, 5, 6, 7],
        ),
    ]


@fixture
def habit_log_list() -> List[HabitLog]:
    return [
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 485, 0, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 520, 0, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 540, 0, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 575, 0, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 720, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 485, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 520, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 540, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 575, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 720, 0, 0),
        ),
    ]


@fixture
def add_habit_log_list(
    session: Session, habit_log_list: List[HabitLog]
) -> List[HabitLog]:
    session.add_all(habit_log_list)
    session.commit()

    return habit_log_list


@fixture
def add_habit_list(
    habit_list: List[Habit],
    session: Session,
    add_user: User,
) -> List[Habit]:
    habit_list_items = []

    for habit in habit_list:
        habit_item = Habit(
            title=habit.title,
            start_time_minutes=habit.start_time_minutes,
            repeat_time_minutes=habit.repeat_time_minutes,
            repeat_days=habit.repeat_days,
            user_id=add_user.id,
        )

        session.add(habit_item)

        habit_list_items.append(habit_item)

    session.commit()

    return habit_list_items
