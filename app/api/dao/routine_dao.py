from datetime import date
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import asc, func
from app.api.errors import DATA_DOES_NOT_EXIST
from app.schemas.routine import RoutineItem, RoutinePublic
from .base import ProtectedBaseDAO
from app.models.models import Routine, RoutineLog


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
                detail=DATA_DOES_NOT_EXIST,
            )

        return routine

    def get_routines(self) -> List[Routine]:
        routines = (
            self.db.query(Routine)
            .filter(
                Routine.user_id == self.user_id,
            )
            .order_by(Routine.start_time_minutes)
            .all()
        )

        return routines

    def get_routines_by_weekday(self, weekday: int) -> List[Routine]:
        routines = (
            self.db.query(Routine)
            .filter(
                Routine.user_id == self.user_id,
                Routine.repeat_days.contains(str(weekday)),
            )
            .order_by(Routine.start_time_minutes)
            .all()
        )

        return routines

    def get_routine_with_elements_by_id(
        self, routine_id: int, date: date
    ) -> RoutinePublic:
        routine = (
            self.db.query(Routine)
            .filter(
                Routine.id == routine_id,
                Routine.user_id == self.user_id,
            )
            .first()
        )

        if not routine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DATA_DOES_NOT_EXIST,
            )

        routine_logs = (
            self.db.query(RoutineLog)
            .filter(
                RoutineLog.routine_id == routine_id,
                func.date(RoutineLog.completed_at) == date,
            )
            .order_by(
                asc(RoutineLog.routine_element_id),
                asc(RoutineLog.completed_at),
            )
            .all()
        )

        routine_with_logs: RoutinePublic = RoutinePublic.from_routine_with_log(
            routine=routine, routine_items=[]
        )
        routine_log_map = dict()
        for log in routine_logs:
            routine_log_map[log.routine_element_id] = log

        for element in routine.routine_elements:
            routine_item = RoutineItem.from_routine_element(element, None)

            if routine_log_map.get(routine_item.id) is not None:
                log = routine_log_map[element.id]
                routine_item.completed_at = log.completed_at
                routine_item.completed_duration_seconds = log.duration_seconds
                routine_item.is_skipped = log.is_skipped

            routine_with_logs.routine_elements.append(routine_item)

        return routine_with_logs

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

    def delete_routine(
        self,
        routine_id: int,
    ) -> None:
        routine = self.get_routine_by_id(routine_id)

        self.db.delete(routine)
