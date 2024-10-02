from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
    Boolean,
    func,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    profile_image = Column(String(100))
    nickname = Column(String(50))
    created_at = Column(TIMESTAMP, default=func.now())


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    order = Column(Integer, nullable=False)
    target_date = Column(TIMESTAMP, default=func.now(), nullable=False)

    content = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )

    completed_at = Column(TIMESTAMP)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )


class Habit(Base):
    __tablename__ = "habit"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)
    end_time_minutes = Column(Integer, nullable=False)
    start_time_minutes = Column(Integer, nullable=False)
    repeat_days = Column(String(7), nullable=False)
    repeat_time_minutes = Column(Integer, nullable=False)

    activated = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    @staticmethod
    def repeat_days_to_string(repeat_days):
        return "".join([str(day) for day in repeat_days])

    def repeat_days_to_list(self):
        return [int(day) for day in self.repeat_days]


class HabitLog(Base):
    __tablename__ = "habit_log"

    id = Column(Integer, primary_key=True)
    completed_at = Column(TIMESTAMP, default=func.now(), nullable=False)

    habit_id = Column(
        Integer, ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )


class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)
    start_time_minutes = Column(Integer, nullable=False)
    repeat_days = Column(String(7), nullable=False)

    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    routine_elements = relationship(
        "RoutineElement",
        order_by="RoutineElement.order.asc()",
        cascade="all, delete",
        lazy="joined",
    )

    def repeat_days_to_list(self):
        return [int(day) for day in self.repeat_days]

    @staticmethod
    def repeat_days_to_string(repeat_days):
        return "".join([str(day) for day in repeat_days])


class RoutineElement(Base):
    __tablename__ = "routine_element"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )

    duration_minutes = Column(Integer)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    deleted_at = Column(TIMESTAMP)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    routine_id = Column(
        Integer, ForeignKey("routine.id", ondelete="CASCADE"), nullable=False
    )


class RoutineLog(Base):
    __tablename__ = "routine_log"

    id = Column(Integer, primary_key=True)

    duration_seconds = Column(Integer, nullable=False)
    completed_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    is_skipped = Column(Boolean, default=False, nullable=False)

    routine_id = Column(
        Integer,
        ForeignKey("routine.id", ondelete="CASCADE"),
        nullable=False,
    )
    routine_element_id = Column(
        Integer,
        ForeignKey("routine_element.id", ondelete="CASCADE"),
        nullable=False,
    )
