from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.api.strings import (
    ROUTINE_DOES_NOT_EXIST_ERROR,
    SERVER_UNTRACKED_ERROR,
)
from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import Routine, RoutineElement, User
from app.repositories import get_routine_repository
from app.repositories.routine_repository import RoutineRepository
from app.schemas.response import Response
from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineItem,
    RoutineUpdateInput,
)

router = APIRouter(
    prefix="/routine",
    tags=["routine"],
    dependencies=[Depends(get_current_user)],
)


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

    routine_elements = [
        RoutineElement(
            user_id=user.id,
            title=item.title,
            order=item.order,
            duration_minutes=item.duration_minutes,
            routine_id=routine.id,
        )
        for item in data.routine_elements
    ]

    commit_and_catch_exception(db, lambda: db.add_all(routine_elements))

    return Response(
        data=RoutineDetail(
            id=routine.id,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=data.repeat_days,
            created_at=routine.created_at,
            updated_at=routine.updated_at,
            deleted_at=None,
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
        ),
        message="Routine created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
)
def get_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    routine = (
        db.query(Routine)
        .options(joinedload(Routine.routine_elements))
        .filter(Routine.id == routine_id, Routine.user_id == user.id)
        .first()
    )

    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ROUTINE_DOES_NOT_EXIST_ERROR,
        )

    response = Response(
        data=RoutineDetail(
            id=routine.id,
            created_at=routine.created_at,
            updated_at=routine.updated_at,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=routine.repeat_days_to_list(),
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
                for item in routine.routine_elements
            ],
        ),
        message="Routine retrieved successfully",
        status_code=status.HTTP_200_OK,
    )

    return response


@router.delete(
    "/{routine_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id, Routine.user_id == user.id)
        .first()
    )

    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ROUTINE_DOES_NOT_EXIST_ERROR,
        )

    try:
        routine.deleted_at = datetime.now()
        db.commit()

        return None
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SERVER_UNTRACKED_ERROR,
        )


def commit_and_catch_exception(db: Session, db_action: callable):
    try:
        db_action()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


@router.put(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
)
def update_routine(
    routine_id: int,
    data: RoutineUpdateInput,
    repository: RoutineRepository = Depends(get_routine_repository),
    user: User = Depends(get_current_user),
):
    routine = repository.update_routine(data)

    return Response(
        data=RoutineDetail.from_routine(routine, routine.routine_elements),
        message="Routine updated successfully",
        status_code=status.HTTP_200_OK,
    )
