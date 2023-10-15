import pytest
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineElement, User

from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineItem,
    RoutineItemUpdate,
    RoutineUpdateInput,
)


@pytest.fixture
def routine_data() -> RoutineCreateInput:
    return RoutineCreateInput(
        title="아침 루틴",
        start_time_minutes=480,
        repeat_days=[1, 2, 3, 4, 5],
        routine_elements=[
            RoutineItemUpdate(title="아침 물 마시기", duration_minutes=5),
            RoutineItemUpdate(title="아침 운동하기", duration_minutes=30),
            RoutineItemUpdate(title="아침 식사하기", duration_minutes=15),
        ],
    )


@pytest.fixture()
def update_routine_only_routine_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_id=1,
        title="점심 루틴",
        start_time_minutes=720,
        repeat_days=[1, 2, 3],
    )


@pytest.fixture()
def update_routine_empty_routine_elements() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_id=1,
        routine_elements=[],
    )


@pytest.fixture()
def update_routine_only_elements_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_id=1,
        routine_elements=[
            RoutineItemUpdate(id=1, title="아침 물 마시기 업데이트", duration_minutes=5),
            RoutineItemUpdate(id=2, title="아침 운동하기 업데이트", duration_minutes=30),
            RoutineItemUpdate(title="추가된 루틴 아이템 1", duration_minutes=10),
            RoutineItemUpdate(title="추가된 루틴 아이템 2", duration_minutes=10),
        ],
    )


@pytest.fixture
def update_routine_all_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_id=1,
        title="점심 루틴",
        start_time_minutes=120,
        repeat_days=[1, 2, 3],
        routine_elements=[
            RoutineItemUpdate(title="점심 물 마시기", duration_minutes=5),
            RoutineItemUpdate(title="점심 운동하기", duration_minutes=30),
        ],
    )


@pytest.fixture
def add_routine(
    session: Session, add_user: User, routine_data: RoutineCreateInput
) -> RoutineDetail:
    repeat_days = "".join([str(day) for day in routine_data.repeat_days])

    test_routine = Routine(
        title=routine_data.title,
        start_time_minutes=routine_data.start_time_minutes,
        repeat_days=repeat_days,
        user_id=add_user.id,
    )

    session.add(test_routine)
    session.commit()

    routine_elements = [
        RoutineElement(
            user_id=add_user.id,
            title=item.title,
            order=index,
            duration_minutes=item.duration_minutes,
            routine_id=test_routine.id,
        )
        for index, item in enumerate(routine_data.routine_elements)
    ]

    session.add_all(routine_elements)
    session.commit()

    return RoutineDetail(
        id=test_routine.id,
        title=test_routine.title,
        start_time_minutes=test_routine.start_time_minutes,
        repeat_days=routine_data.repeat_days,
        created_at=test_routine.created_at,
        updated_at=test_routine.updated_at,
        routine_elements=[
            RoutineItem(
                id=item.id,
                title=item.title,
                duration_minutes=item.duration_minutes,
                created_at=item.created_at,
                updated_at=item.updated_at,
                completed=False,
            )
            for item in routine_elements
        ],
    )
