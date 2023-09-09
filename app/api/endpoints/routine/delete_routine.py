from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.strings import (
    ROUTINE_DOES_NOT_EXIST_ERROR,
    SERVER_UNTRACKED_ERROR,
)
from app.core.auth import get_current_user

from . import router
from app.database.db import get_db
from app.models.models import Routine, User


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
