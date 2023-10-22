from sqlalchemy.orm import Session

from app.dao.routine_dao import RoutineDAO
from app.dao.routine_element_dao import RoutineElementDAO
from app.models.models import Routine, User
from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineUpdateInput,
)

from .base import ProtectedBaseRepository


class RoutineRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user: User):
        super().__init__(db, user)

        self.routine_dao = RoutineDAO(db=db, user=user)
        self.routine_element_dao = RoutineElementDAO(db=db, user=user)

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

    def create_routine(self, routine: RoutineCreateInput) -> RoutineDetail:
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

        return RoutineDetail.from_routine(
            routine=new_routine, routine_elements=routine_elements
        )
