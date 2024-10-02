from datetime import datetime
from typing import List
import pytest
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineElement, RoutineLog, User

from app.schemas.routine import (
    RoutineCreateInput,
    RoutinePublic,
    RoutineItem,
    RoutineItemUpdate,
    RoutineLogBase,
    RoutineUpdateInput,
)


@pytest.fixture
def routine_data() -> RoutineCreateInput:
    return RoutineCreateInput(
        title="아침 루틴",
        start_time_minutes=480,
        repeat_days=[0, 1, 2, 3, 4],
        routine_elements=[
            RoutineItemUpdate(title="아침 물 마시기", duration_minutes=5),
            RoutineItemUpdate(title="아침 운동하기", duration_minutes=30),
            RoutineItemUpdate(title="아침 식사하기", duration_minutes=15),
            RoutineItemUpdate(title="세수하기", duration_minutes=15),
        ],
    )


@pytest.fixture
def update_routine_only_routine_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        title="점심 루틴",
        start_time_minutes=720,
        repeat_days=[0, 1, 2],
    )


@pytest.fixture
def update_routine_empty_routine_elements() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_elements=[],
    )


@pytest.fixture
def update_routine_only_elements_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        routine_elements=[
            RoutineItemUpdate(
                id=1, title="아침 물 마시기 업데이트", duration_minutes=5
            ),
            RoutineItemUpdate(
                id=2, title="아침 운동하기 업데이트", duration_minutes=30
            ),
            RoutineItemUpdate(
                title="추가된 루틴 아이템 1", duration_minutes=10
            ),
            RoutineItemUpdate(
                title="추가된 루틴 아이템 2", duration_minutes=10
            ),
        ],
    )


@pytest.fixture
def update_routine_all_data() -> RoutineUpdateInput:
    return RoutineUpdateInput(
        title="점심 루틴",
        start_time_minutes=120,
        repeat_days=[0, 1, 2],
        routine_elements=[
            RoutineItemUpdate(title="점심 물 마시기", duration_minutes=5),
            RoutineItemUpdate(title="점심 운동하기", duration_minutes=30),
        ],
    )


@pytest.fixture
def add_routine(
    session: Session, add_user: User, routine_data: RoutineCreateInput
) -> RoutinePublic:
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

    return RoutinePublic(
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
                is_skipped=False,
            )
            for item in routine_elements
        ],
    )


@pytest.fixture
def routine_log_data(
    session: Session, add_routine: RoutinePublic
) -> List[RoutineLogBase]:
    return [
        RoutineLogBase(
            routine_item_id=1,
            duration_seconds=5 * 60,
        ),
        RoutineLogBase(
            routine_item_id=2,
            duration_seconds=30 * 60,
        ),
        RoutineLogBase(
            routine_item_id=3,
            duration_seconds=30 * 60,
        ),
        RoutineLogBase(
            routine_item_id=4,
            duration_seconds=30 * 60,
            is_skipped=True,
        ),
    ]


@pytest.fixture
def target_date():
    return datetime(2024, 7, 24)


@pytest.fixture
def non_target_date():
    return datetime(2024, 7, 27)


@pytest.fixture
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
        Routine(
            title="test_routine",
            start_time_minutes=540,
            repeat_days="0",
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
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=2,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=3,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=1,
            routine_element_id=4,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=target_date,
            duration_seconds=5 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=target_date,
            duration_seconds=15 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=target_date,
            duration_seconds=15 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=target_date,
            duration_seconds=15 * 60,
            is_skipped=True,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=target_date,
            duration_seconds=15 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=1,
            completed_at=non_target_date,
            duration_seconds=15 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=2,
            completed_at=non_target_date,
            duration_seconds=15 * 60,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=3,
            completed_at=non_target_date,
            duration_seconds=15 * 60,
            is_skipped=True,
        ),
        RoutineLog(
            routine_id=2,
            routine_element_id=4,
            completed_at=non_target_date,
            duration_seconds=15 * 60,
        ),
    ]

    session.add_all(routine_log_list)
    session.commit()

    return routine_list
