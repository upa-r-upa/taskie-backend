from typing import List
from fastapi import HTTPException, status
from app.api.strings import ROUTINE_DOES_NOT_EXIST_ERROR
from app.dao.base import ProtectedBaseDAO
from app.models.models import Routine
from sqlalchemy.exc import SQLAlchemyError


class RoutineDAO(ProtectedBaseDAO):
    def get_routine_by_id(self, routine_id: int) -> Routine:
        routine = (
            self.db.query(Routine)
            .filter(Routine.id == routine_id, Routine.user_id == self.user_id)
            .first()
        )

        if not routine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ROUTINE_DOES_NOT_EXIST_ERROR,
            )

        return routine

    def update_routine(
        self,
        routine_id: int,
        title: str | None,
        start_time_minutes: int | None,
        repeat_days: List[int] | None,
    ) -> Routine:
        routine = self.get_routine_by_id(routine_id)

        try:
            routine.title = title or routine.title
            routine.start_time_minutes = (
                start_time_minutes or routine.start_time_minutes
            )
            routine.repeat_days = (
                repeat_days and routine.repeat_days_to_string(repeat_days)
            ) or routine.repeat_days

            self.db.commit()

            return routine
        except SQLAlchemyError:
            self.db.rollback()

            raise Exception("Failed to update routine")
