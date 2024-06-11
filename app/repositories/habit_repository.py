from pytest import Session

from app.models.models import Habit, User
from app.schemas.habit import HabitCreateInput

from .base import ProtectedBaseRepository


class HabitRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user: User):
        super().__init__(db, user)

    def create_habit(self, habit: HabitCreateInput) -> Habit:
        new_habit = Habit(
            title=habit.title,
            start_time_minutes=habit.start_time_minutes,
            end_time_minutes=habit.end_time_minutes,
            repeat_time_minutes=habit.repeat_time_minutes,
            repeat_days=Habit.repeat_days_to_string(habit.repeat_days),
            user_id=self.user_id,
        )

        self.db.add(new_habit)

        return new_habit
