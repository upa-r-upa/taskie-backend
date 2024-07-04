from sqlalchemy import desc, func
from pytest import Session

from app.models.models import Habit, HabitLog, User
from app.schemas.habit import HabitCreateInput, HabitWithLog

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

    def get_habits(
        self,
        limit: int,
        log_target_date: str,
        last_id: int = None,
        deleted: bool = False,
        activated: bool = True,
    ) -> list[HabitWithLog]:
        query = self.db.query(Habit).filter(
            Habit.user_id == self.user_id,
            Habit.activated == int(activated),
        )

        if deleted:
            query = query.filter(Habit.deleted_at.isnot(None))

        if last_id is not None:
            query = query.filter(Habit.id < last_id)

        habits = query.order_by(desc(Habit.id)).limit(limit).all()

        for habit in habits:
            logs = (
                habit.habit_logs.filter(
                    func.date(HabitLog.completed_at) == log_target_date
                )
                .order_by(desc(HabitLog.id))
                .all()
            )
            habit.log_list = logs

        return [HabitWithLog.from_orm(habit) for habit in habits]
