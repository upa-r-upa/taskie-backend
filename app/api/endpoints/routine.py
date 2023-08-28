from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user

from app.database.db import get_db
from app.models.models import Routine, RoutineElement
from app.schemas.response import Response
from app.schemas.routine import RoutineCreateInput, RoutineDetail, RoutineItem

router = APIRouter(
    prefix="/routine",
    tags=["routine"],
    dependencies=[Depends(get_current_user)],
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
    user=Depends(get_current_user),
):
    repeat_days = "".join([str(day) for day in data.repeat_days])

    routine = Routine(
        title=data.title,
        start_time_minutes=data.start_time_minutes,
        repeat_days=repeat_days,
        user_id=user.id,
    )

    commit_and_catch_exception(db, lambda: db.add(routine))

    routine_items = [
        RoutineElement(
            title=item.title,
            order=item.order,
            duration_minutes=item.duration_minutes,
            routine_id=routine.id,
        )
        for item in data.routine_items
    ]

    commit_and_catch_exception(db, lambda: db.add_all(routine_items))

    return Response(
        data=RoutineDetail(
            id=routine.id,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=data.repeat_days,
            created_at=routine.created_at,
            updated_at=routine.updated_at,
            routine_items=[
                RoutineItem(
                    id=item.id,
                    title=item.title,
                    order=item.order,
                    duration_minutes=item.duration_minutes,
                    created_at=item.created_at,
                    updated_at=item.updated_at,
                    completed=False,
                )
                for item in routine_items
            ],
        ),
        message="Routine created successfully",
        status_code=status.HTTP_201_CREATED,
    )
