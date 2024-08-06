from typing import List

from sqlalchemy import func

from app.dao.base import ProtectedBaseDAO
from app.models.models import RoutineLog
from app.schemas.routine import RoutineLogBase


class RoutineLogDAO(ProtectedBaseDAO):
    def get_routine_logs_by_date(
        self, routine_id: int, target_date: str
    ) -> List[RoutineLog]:
        log = (
            self.db.query(RoutineLog)
            .filter(
                RoutineLog.routine_id == routine_id,
                target_date == func.date(RoutineLog.completed_at),
            )
            .all()
        )

        return log

    def put_logs(self, routine_id: int, logs: List[RoutineLogBase]):
        for log in logs:
            routine_log = RoutineLog(
                routine_id=routine_id,
                routine_element_id=log.routine_item_id,
                duration_minutes=log.duration_minutes,
                is_skipped=bool(log.is_skipped),
            )

            self.db.add(routine_log)

        return routine_log
