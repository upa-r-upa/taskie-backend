from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.api.strings import ROUTINE_DOES_NOT_EXIST_ERROR
from app.core.auth import get_current_user

from . import router
from app.database.db import get_db
from app.models.models import Routine, User
from app.schemas.response import Response
from app.schemas.routine import (
    RoutineDetail,
    RoutineItem,
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
