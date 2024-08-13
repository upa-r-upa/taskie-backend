from datetime import datetime
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
        activated: bool = True,
    ) -> list[HabitWithLog]:
        weekday = datetime.strptime(log_target_date, "%Y-%m-%d").weekday()
        query = self.db.query(Habit).filter(
            Habit.user_id == self.user_id,
            Habit.activated == activated,
        )

        if last_id is not None:
            query = query.filter(Habit.id < last_id)

        habits = query.order_by(desc(Habit.id)).limit(limit).all()

        result_habit_list = []
        for habit in habits:
            habit_with_logs: HabitWithLog = HabitWithLog.from_orm_with_weekday(
                habit, [], weekday
            )
            logs = (
                habit.habit_logs.filter(
                    func.date(HabitLog.completed_at) == log_target_date
                )
                .order_by(desc(HabitLog.id))
                .all()
            )
            habit_with_logs.log_list = logs
            result_habit_list.append(habit_with_logs)

        return result_habit_list

    def _get_weekday_sorted_habits(
        self, habit_list: list[HabitWithLog], weekday: int
    ) -> list[Habit]:
        def sort_key(habit: HabitWithLog):
            difference = (habit.near_weekday - weekday) % 6
            return difference

        return sorted(habit_list, key=sort_key)

    def get_habits_by_date(self, date: str) -> list[HabitWithLog]:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        habits = (
            self.db.query(Habit)
            .filter(
                Habit.user_id == self.user_id,
                Habit.repeat_days.contains(date_obj.weekday()),
            )
            .order_by(desc(Habit.id))
            .all()
        )

        log_map = dict()
        for habit in habits:
            logs = (
                habit.habit_logs.filter(
                    func.date(HabitLog.completed_at) == date
                )
                .order_by(desc(HabitLog.id))
                .all()
            )
            log_map[habit.id] = logs

        habit_with_log = [
            HabitWithLog.from_orm_with_weekday(
                habit, log_map[habit.id], date_obj.weekday()
            )
            for habit in habits
        ]
        return habit_with_log
