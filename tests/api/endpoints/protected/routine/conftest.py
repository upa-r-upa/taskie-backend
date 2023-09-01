import pytest
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineElement, User

from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineItem,
    RoutineItemBase,
)


@pytest.fixture
def routine() -> RoutineCreateInput:
    return RoutineCreateInput(
        title="아침 루틴",
        start_time_minutes=480,
        repeat_days=[1, 2, 3, 4, 5],
        routine_elements=[
            RoutineItemBase(title="아침 물 마시기", duration_minutes=5, order=1),
            RoutineItemBase(title="아침 운동하기", duration_minutes=30, order=2),
            RoutineItemBase(title="아침 식사하기", duration_minutes=15, order=3),
        ],
    )


@pytest.fixture
def add_routine(
    session: Session, add_user: User, routine: RoutineCreateInput
) -> RoutineDetail:
    repeat_days = "".join([str(day) for day in routine.repeat_days])

    test_routine = Routine(
        title=routine.title,
        start_time_minutes=routine.start_time_minutes,
        repeat_days=repeat_days,
        user_id=add_user.id,
    )

    session.add(test_routine)
    session.commit()

    routine_elements = [
        RoutineElement(
            title=item.title,
            order=item.order,
            duration_minutes=item.duration_minutes,
            routine_id=test_routine.id,
        )
        for item in routine.routine_elements
    ]

    session.add_all(routine_elements)
    session.commit()

    return RoutineDetail(
        id=test_routine.id,
        title=test_routine.title,
        start_time_minutes=test_routine.start_time_minutes,
        repeat_days=routine.repeat_days,
        created_at=test_routine.created_at,
        updated_at=test_routine.updated_at,
        routine_elements=[
            RoutineItem(
                id=item.id,
                title=item.title,
                order=item.order,
                duration_minutes=item.duration_minutes,
                created_at=item.created_at,
                updated_at=item.updated_at,
                completed=False,
            )
            for item in routine_elements
        ],
    )
