from datetime import date
from typing import Optional
from sqlalchemy import desc, func
from pytest import Session

from app.exceptions.exceptions import DataNotFoundError
from app.models.models import Habit, HabitLog
from app.schemas.habit import HabitCreateInput, HabitUpdateInput, HabitWithLog

from .base import ProtectedBaseRepository


class HabitRepository(ProtectedBaseRepository):
    def __init__(self, db: Session, user_id: int):
        super().__init__(db, user_id)

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
        weekday: int,
        last_id: int = None,
        activated: bool = True,
    ):
        query = self.db.query(Habit).filter(
            Habit.user_id == self.user_id,
            Habit.activated == activated,
        )

        if last_id is not None:
            query = query.filter(Habit.id < last_id)

        habits = query.order_by(desc(Habit.id)).limit(limit).all()

        return habits

    def get_habit_logs_by_date(
        self,
        habit_ids: list[str],
        date: date,
    ):
        logs = (
            self.db.query(HabitLog)
            .filter(
                func.date(HabitLog.completed_at) == date,
                HabitLog.habit_id.in_(habit_ids),
            )
            .order_by(desc(HabitLog.id))
            .all()
        )

        return logs

    def _combine_habits_and_logs(
        self, habits: list[Habit], logs: list[HabitLog], weekday: int
    ):
        logs_by_habit_id = {}

        for log in logs:
            if log.habit_id not in logs_by_habit_id:
                logs_by_habit_id[log.habit_id] = []
            logs_by_habit_id[log.habit_id].append(log)

        result_habits = []

        for habit in habits:
            habit_logs = logs_by_habit_id.get(habit.id, [])
            habit_with_logs: HabitWithLog = HabitWithLog.from_orm_with_weekday(
                habit, habit_logs, weekday
            )
            result_habits.append(habit_with_logs)

        return result_habits

    def get_habits_with_date_logs(
        self,
        limit: int,
        log_target_date: date,
        last_id: int = None,
        activated: bool = True,
    ) -> list[HabitWithLog]:
        habits = self.get_habits(
            limit, log_target_date.weekday(), last_id, activated
        )
        habit_ids = [habit.id for habit in habits]
        habit_logs = self.get_habit_logs_by_date(habit_ids, log_target_date)

        result_habits = self._combine_habits_and_logs(
            habits, habit_logs, log_target_date.weekday()
        )

        return result_habits

    def _sorted_habits_by_weekday(
        self, habit_list: list[HabitWithLog], weekday: int
    ) -> list[Habit]:
        def sort_key(habit: HabitWithLog):
            difference = (habit.near_weekday - weekday) % 6
            return difference

        return sorted(habit_list, key=sort_key)

    def get_habits_by_weekday(self, weekday: int):
        habits = (
            self.db.query(Habit)
            .filter(
                Habit.user_id == self.user_id,
                Habit.activated,
                Habit.repeat_days.contains(weekday),
            )
            .order_by(desc(Habit.id))
            .all()
        )

        return habits

    def get_habits_with_log_by_date(self, target: date) -> list[HabitWithLog]:
        habits = self.get_habits_by_weekday(target.weekday())
        habit_ids = [habit.id for habit in habits]

        habits_logs = self.get_habit_logs_by_date(habit_ids, target)
        habit_with_log = self._combine_habits_and_logs(
            habits, habits_logs, target.weekday()
        )
        return habit_with_log

    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        habit = (
            self.db.query(Habit)
            .filter(Habit.id == habit_id, Habit.user_id == self.user_id)
            .first()
        )

        return habit

    def delete_habit(self, habit_id: int):
        habit = self.get_habit_by_id(habit_id)

        if not habit:
            raise DataNotFoundError()

        self.db.delete(habit)

        return None

    def update_habit(self, habit_id: int, update_input: HabitUpdateInput):
        habit = self.get_habit_by_id(habit_id)

        if not habit:
            raise DataNotFoundError()

        habit.title = update_input.title
        habit.start_time_minutes = update_input.start_time_minutes
        habit.end_time_minutes = update_input.end_time_minutes
        habit.repeat_time_minutes = update_input.repeat_time_minutes
        habit.repeat_days = Habit.repeat_days_to_string(
            update_input.repeat_days
        )
        habit.activated = update_input.activated

        return habit

    def achieve_habit(self, habit_id: int) -> HabitLog:
        habit = self.get_habit_by_id(habit_id)

        if not habit:
            raise DataNotFoundError()

        log = HabitLog(habit_id=habit_id)

        self.db.add(log)

        return log
