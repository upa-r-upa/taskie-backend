from datetime import date
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from app.api.dao.routine_dao import RoutineDAO
from app.api.dao.routine_element_dao import RoutineElementDAO
from app.api.dao.routine_log_dao import RoutineLogDAO
from app.models.models import Routine, RoutineLog, User
from app.schemas.routine import (
    RoutineCreateInput,
    RoutinePublic,
    RoutineItem,
    RoutineUpdateInput,
)

from .base import ProtectedBaseRepository


class RoutineRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user: User):
        super().__init__(db, user)

        self.routine_dao = RoutineDAO(db=db, user=user)
        self.routine_element_dao = RoutineElementDAO(db=db, user=user)
        self.routine_log_dao = RoutineLogDAO(db=db, user=user)

    def update_routine(
        self, routine_id: int, routine: RoutineUpdateInput
    ) -> Routine:
        updated_routine = self.routine_dao.update_routine(
            routine_id=routine_id,
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=routine.repeat_days,
        )

        self.routine_element_dao.update_routine_elements(
            routine_id=routine_id,
            routine_elements=updated_routine.routine_elements or [],
            updates_routine_elements=routine.routine_elements or [],
        )

        self.db.flush()

        return updated_routine

    def create_routine(self, routine: RoutineCreateInput) -> RoutinePublic:
        new_routine = self.routine_dao.create_routine(
            title=routine.title,
            start_time_minutes=routine.start_time_minutes,
            repeat_days=routine.repeat_days,
        )

        self.db.flush()

        routine_elements = self.routine_element_dao.create_routine_elements(
            routine_id=new_routine.id,
            routine_elements=routine.routine_elements,
        )

        self.db.flush()

        return RoutinePublic.from_routine(
            routine=new_routine, routine_elements=routine_elements
        )

    def _get_routines_with_logs(
        self, routines: list[Routine], target: date
    ) -> list[RoutinePublic]:
        routine_ids = [routine.id for routine in routines]
        routine_logs = (
            self.db.query(RoutineLog)
            .filter(
                RoutineLog.routine_id.in_(routine_ids),
                func.date(RoutineLog.completed_at) == target,
            )
            .order_by(
                desc(RoutineLog.routine_id),
                asc(RoutineLog.routine_element_id),
                asc(RoutineLog.completed_at),
            )
            .all()
        )

        routine_log_map = {}
        for log in routine_logs:
            if routine_log_map.get(log.routine_id) is None:
                routine_log_map[log.routine_id] = {}

            routine_log_map[log.routine_id][log.routine_element_id] = log

        result_routine_list = []
        for routine in routines:
            routine_with_logs = RoutinePublic.from_routine_with_log(
                routine=routine, routine_items=[]
            )
            for element in routine.routine_elements:
                routine_item = RoutineItem.from_routine_element(element, None)

                if (
                    routine_log_map.get(routine.id) is not None
                    and routine_log_map[routine.id].get(routine_item.id)
                    is not None
                ):
                    log = routine_log_map[routine.id][element.id]
                    routine_item.completed_at = log.completed_at
                    routine_item.completed_duration_seconds = (
                        log.duration_seconds
                    )
                    routine_item.is_skipped = log.is_skipped

                routine_with_logs.routine_elements.append(routine_item)

            result_routine_list.append(routine_with_logs)

        return result_routine_list

    def get_routine_list(self, target: date) -> list[RoutinePublic]:
        routines = self.routine_dao.get_routines()
        return self._get_routines_with_logs(routines, target)

    def get_routine_by_date(self, target: date) -> list[RoutinePublic]:
        routines = self.routine_dao.get_routines_by_weekday(
            weekday=target.weekday()
        )
        return self._get_routines_with_logs(routines, target)
