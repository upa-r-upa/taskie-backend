from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.core.utils import get_user_by_username

from app.database.db import get_db
from app.models.models import Routine, RoutineRepeatDay, Todo, TodoRoutine
from app.schemas.response import Response
from app.schemas.routine import RoutineCreateInput, RoutineDetail, RoutineItem

router = APIRouter(
    prefix="/routine", tags=["routine"], dependencies=[Depends(get_current_user)]
)


def commit_and_catch_exception(db: Session, db_action: callable):
    try:
        db_action()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


@router.post(
    "/create",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_201_CREATED,
)
def create_routine(
    data: RoutineCreateInput,
    db: Session = Depends(get_db),
    username=Depends(get_current_user),
):
    user = get_user_by_username(db, username)

    routine = Routine(
        title=data.title,
        start_time_minutes=data.start_time_minutes,
        user_id=user.id,
    )

    commit_and_catch_exception(db, lambda: db.add(routine))

    routine_repeat_days = [
        RoutineRepeatDay(routine_id=routine.id, day=day, user_id=user.id)
        for day in data.repeat_days
    ]

    commit_and_catch_exception(db, lambda: db.bulk_save_objects(routine_repeat_days))

    todo_items = [
        Todo(title=todo_item.title, user_id=user.id) for todo_item in data.todo_items
    ]

    commit_and_catch_exception(
        db, lambda: db.bulk_save_objects(todo_items, return_defaults=True)
    )

    routine_items = []

    for index, todo_item in enumerate(data.todo_items):
        routine_item = TodoRoutine(
            routine_id=routine.id,
            todo_id=todo_items[index].id,
            duration_minutes=todo_item.duration_minutes,
            user_id=user.id,
        )

        routine_items.append(routine_item)

    commit_and_catch_exception(db, lambda: db.add_all(routine_items))

    return Response(
        data=RoutineDetail(
            id=routine.id,
            created_at=routine.created_at,
            todo_items=[
                RoutineItem(
                    title=todo_item.title,
                    duration_minutes=routine_item.duration_minutes,
                    id=routine_item.id,
                    created_at=routine_item.created_at,
                    updated_at=routine_item.updated_at,
                )
                for routine_item, todo_item in zip(routine_items, todo_items)
            ],
        ),
        message="Routine created successfully",
        status_code=status.HTTP_201_CREATED,
    )
