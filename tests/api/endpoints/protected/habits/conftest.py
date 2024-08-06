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
        repeat_days=[0, 1, 2, 3, 4, 5, 6],
    )


@fixture
def habit_list() -> List[Habit]:
    return [
        Habit(
            title="습관 1",
            start_time_minutes=480,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 12, 7, 0, 0),
        ),
        Habit(
            title="습관 2",
            start_time_minutes=600,
            end_time_minutes=1380,
            repeat_time_minutes=60,
            repeat_days="01234",
            created_at=datetime(2024, 6, 12, 8, 0, 0),
        ),
        Habit(
            title="습관 3",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 12, 9, 0, 0),
        ),
        Habit(
            title="습관 4",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 13, 0, 0, 0),
        ),
        Habit(
            title="습관 5",
            start_time_minutes=960,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 13, 5, 0, 0),
        ),
        Habit(
            title="습관 6 (비활성화)",
            start_time_minutes=480,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 13, 7, 0, 0),
            activated=0,
        ),
        Habit(
            title="습관 7 (삭제)",
            start_time_minutes=480,
            end_time_minutes=1380,
            repeat_time_minutes=30,
            repeat_days="0123456",
            created_at=datetime(2024, 6, 13, 8, 0, 0),
            activated=0,
            deleted_at=datetime(2024, 6, 13, 8, 0, 0),
        ),
    ]


@fixture
def habit_log_list() -> List[HabitLog]:
    return [
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 8, 30, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 8, 50, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 8, 59, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 12, 35, 0),
        ),
        HabitLog(
            habit_id=1,
            completed_at=datetime(2024, 6, 12, 13, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 14, 8, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 15, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 16, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 17, 0, 0),
        ),
        HabitLog(
            habit_id=2,
            completed_at=datetime(2024, 6, 12, 18, 0, 0),
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
        habit.user_id = add_user.id

        session.add(habit)
        habit_list_items.append(habit)

    session.commit()

    return habit_list_items
