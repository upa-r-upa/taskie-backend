from datetime import datetime
from typing import List

from app.dao.base import ProtectedBaseDAO
from app.models.models import RoutineLog


class RoutineLogDAO(ProtectedBaseDAO):
    def _is_timestamp_on_day(date: datetime, target_timestamp: datetime):
        timestamp_date = target_timestamp.date()

        return date == timestamp_date

    def get_routine_log_by_date(
        self, element_id: int, target_date: datetime
    ) -> RoutineLog | None:
        log = (
            self.db.query(RoutineLog)
            .filter(
                RoutineLog.routine_element_id == element_id,
                self._is_timestamp_on_day(
                    target_date, RoutineLog.completed_at
                ),
            )
            .first()
        )

        return log

    def update_logs_complete(self, completed: bool, item_ids: List[int]):
        current_date = datetime.now().date()

        for item_id in item_ids:
            log = self.get_routine_log_by_date(item_id, current_date)

            if completed:
                self.add_log(item_id, log)
            else:
                self.remove_log(log)

    def add_log(self, item_id: int, log: RoutineLog | None):
        if log is None:
            log = RoutineLog(
                routine_element_id=item_id,
            )

            self.db.add(log)

    def remove_log(self, log: RoutineLog | None):
        if log is not None:
            self.db.delete(log)
