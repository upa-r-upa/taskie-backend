from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from app.api.strings import ROUTINE_DOES_NOT_EXIST_ERROR
from app.dao.base import ProtectedBaseDAO
from app.models.models import Routine


class RoutineDAO(ProtectedBaseDAO):
    def get_routine_by_id(self, routine_id: int) -> Routine:
        routine = (
            self.db.query(Routine)
            .filter(
                Routine.id == routine_id,
                Routine.user_id == self.user_id,
                Routine.deleted_at.is_(None),
            )
            .first()
        )

        if not routine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ROUTINE_DOES_NOT_EXIST_ERROR,
            )

        return routine

    def get_routine_with_elements_by_id(self, routine_id: int) -> Routine:
        routine = (
            self.db.query(Routine)
            .options(joinedload(Routine.routine_elements))
            .filter(
                Routine.id == routine_id,
                Routine.user_id == self.user_id,
                Routine.deleted_at.is_(None),
            )
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

        routine.title = title or routine.title
        routine.start_time_minutes = (
            start_time_minutes or routine.start_time_minutes
        )
        routine.repeat_days = (
            repeat_days and routine.repeat_days_to_string(repeat_days)
        ) or routine.repeat_days

        return routine

    def create_routine(
        self,
        title: str,
        start_time_minutes: int,
        repeat_days: List[int],
    ) -> Routine:
        routine = Routine(
            title=title,
            start_time_minutes=start_time_minutes,
            repeat_days=Routine.repeat_days_to_string(repeat_days),
            user_id=self.user_id,
        )

        self.db.add(routine)

        return routine

    def soft_delete_routine(
        self,
        routine_id: int,
    ) -> None:
        routine = self.get_routine_by_id(routine_id)

        routine.deleted_at = datetime.now()
