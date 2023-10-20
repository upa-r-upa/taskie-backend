from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.dao.routine_dao import RoutineDAO
from app.dao.routine_element_dao import RoutineElementDAO
from app.models.models import Routine
from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineUpdateInput,
)

from .base import ProtectedBaseRepository


class RoutineRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user_id: int):
        super().__init__(db, user_id)

        self.routine_dao = RoutineDAO(db, user_id)
        self.routine_element_dao = RoutineElementDAO(db, user_id)

    def update_routine(self, routine: RoutineUpdateInput) -> Routine:
        try:
            updated_routine = self.routine_dao._update_routine(
                routine_id=routine.routine_id,
                title=routine.title,
                start_time_minutes=routine.start_time_minutes,
                repeat_days=routine.repeat_days,
            )

            self.routine_element_dao._update_routine_elements(
                routine_id=routine.routine_id,
                routine_elements=updated_routine.routine_elements or [],
                updates_routine_elements=routine.routine_elements or [],
            )

        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Failed to update routine")

        else:
            self.db.commit()

        return updated_routine

    def create_routine(self, routine: RoutineCreateInput) -> RoutineDetail:
        try:
            new_routine = self.routine_dao._create_routine(
                title=routine.title,
                start_time_minutes=routine.start_time_minutes,
                repeat_days=routine.repeat_days,
            )

            routine_elements = (
                self.routine_element_dao._create_routine_elements(
                    routine_id=new_routine.id,
                    routine_elements=routine.routine_elements,
                )
            )
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Failed to create routine")

        else:
            self.db.commit()

        return RoutineDetail.from_routine(
            routine=new_routine, routine_elements=routine_elements
        )
