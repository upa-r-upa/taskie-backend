from datetime import datetime
from pytest import fixture
from sqlalchemy.orm import Session

from app.models.models import (
    Habit,
    HabitLog,
    Routine,
    RoutineElement,
    RoutineLog,
    Todo,
    User,
)


@fixture
def target_date():
    return datetime(2024, 7, 24)


@fixture
def non_target_date():
    return datetime(2024, 7, 27)


@fixture
def add_todo_list(
    session: Session,
    add_user: User,
    target_date: datetime,
    non_target_date: datetime,
):
    todo_list = [
        Todo(
            title="test_todo_1",
            content="test_todo_1_content",
            order=1,
            user_id=add_user.id,
            target_date=target_date,
        ),
        Todo(
            title="test_todo_2",
            content="test_todo_2_content",
            order=2,
            user_id=add_user.id,
            target_date=non_target_date,
            completed_at=target_date,
        ),
        Todo(
            title="test_todo_3",
            content="test_todo_3_content",
            order=3,
            user_id=add_user.id,
            target_date=non_target_date,
        ),
        Todo(
            title="test_todo_4",
            content="test_todo_4_content",
            order=4,
            user_id=add_user.id,
            target_date=target_date,
            completed_at=target_date,
        ),
        Todo(
            title="test_todo_5",
            content="test_todo_5_content",
            order=5,
            user_id=add_user.id,
            target_date=target_date,
            completed_at=target_date,
        ),
        Todo(
            title="test_todo_6",
            content="test_todo_6_content",
            order=6,
            user_id=add_user.id,
            target_date=target_date,
        ),
    ]

    session.add_all(todo_list)
    session.commit()

    return todo_list


@fixture
def add_habit_list_with_log(
    session: Session,
    add_user: User,
    target_date: datetime,
    non_target_date: datetime,
):
    habit_list = [
        Habit(
            title="test_habit",
            start_time_minutes=540,
            end_time_minutes=1260,
            repeat_time_minutes=60,
            repeat_days="01",
            user_id=add_user.id,
        ),
        Habit(
            title="test_habit",
            start_time_minutes=540,
            end_time_minutes=1260,
            repeat_time_minutes=60,
            repeat_days="0",
            user_id=add_user.id,
        ),
        Habit(
            title="test_habit",
            start_time_minutes=540,
            end_time_minutes=1260,
            repeat_time_minutes=60,
            repeat_days="0123456",
            user_id=add_user.id,
        ),
        Habit(
            title="test_habit",
            start_time_minutes=540,
            end_time_minutes=1260,
            repeat_time_minutes=60,
            repeat_days="0123456",
            user_id=add_user.id,
        ),
    ]

    session.add_all(habit_list)
    session.commit()

    habit_log_list = [
        HabitLog(
            habit_id=3,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=3,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=3,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=3,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=target_date,
        ),
        HabitLog(
            habit_id=4,
            completed_at=non_target_date,
        ),
    ]

    session.add_all(habit_log_list)
    session.commit()

    return habit_list


@fixture
def add_routine_list_with_log(
    session: Session,
    add_user: User,
    target_date: datetime,
    non_target_date: datetime,
):
    routine_list = [
        Routine(
            title="test_routine",
            start_time_minutes=540,
            repeat_days="0123456",
            user_id=add_user.id,
        ),
        Routine(
            title="test_routine",
            start_time_minutes=540,
            repeat_days="0123456",
            user_id=add_user.id,
        ),
        Routine(
            title="test_routine",
            start_time_minutes=540,
            repeat_days="0123456",
            user_id=add_user.id,
        ),
    ]

    session.add_all(routine_list)
    session.commit()

    routine_element_list = [
        RoutineElement(
            routine_id=1,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=1,
        ),
        RoutineElement(
            routine_id=1,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=2,
        ),
        RoutineElement(
            routine_id=1,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=3,
        ),
        RoutineElement(
            routine_id=1,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=4,
        ),
        RoutineElement(
            routine_id=2,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=1,
        ),
        RoutineElement(
            routine_id=2,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=2,
        ),
        RoutineElement(
            routine_id=2,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=3,
        ),
        RoutineElement(
            routine_id=2,
            user_id=add_user.id,
            title="test_routine_element",
            duration_minutes=10,
            order=4,
        ),
    ]

    session.add_all(routine_element_list)
    session.commit()

    routine_log_list = [
        RoutineLog(
            routine_id=1,
            routine_element_id=1,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=2,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=3,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=4,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=target_date,
            duration_minutes=5,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=target_date,
            duration_minutes=15,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=target_date,
            duration_minutes=15,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=target_date,
            duration_minutes=15,
            is_skipped=True,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=target_date,
            duration_minutes=15,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=non_target_date,
            duration_minutes=15,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=non_target_date,
            duration_minutes=15,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=non_target_date,
            duration_minutes=15,
            is_skipped=1,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=non_target_date,
            duration_minutes=15,
        ),
    ]

    session.add_all(routine_log_list)
    session.commit()

    return routine_list
