from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
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

    todos = relationship(
        "Todo", back_populates="user", lazy="dynamic", cascade="all, delete"
    )
    habits = relationship(
        "Habit", back_populates="user", lazy="dynamic", cascade="all, delete"
    )
    routines = relationship(
        "Routine", back_populates="user", lazy="dynamic", cascade="all, delete"
    )


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    target_date = Column(TIMESTAMP, default=func.now())
    order = Column(Integer, nullable=False)

    completed_at = Column(TIMESTAMP)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="todos")


class Habit(Base):
    __tablename__ = "habit"

    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    end_time_minutes = Column(Integer, nullable=False)
    start_time_minutes = Column(Integer, nullable=False)
    repeat_days = Column(Text, nullable=False)
    repeat_time_minutes = Column(Integer, nullable=False)

    activated = Column(Integer, default=1)
    deleted_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="habits")
    habit_logs = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete",
        lazy="dynamic",
    )

    @staticmethod
    def repeat_days_to_string(repeat_days):
        return "".join([str(day) for day in repeat_days])

    def repeat_days_to_list(self):
        return [int(day) for day in self.repeat_days]


class HabitLog(Base):
    __tablename__ = "habit_log"

    id = Column(Integer, primary_key=True)

    completed_at = Column(TIMESTAMP, onupdate=func.now())

    habit_id = Column(
        Integer, ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )
    habit = relationship("Habit", back_populates="habit_logs")


class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True)

    title = Column(Text, nullable=False)
    start_time_minutes = Column(Integer, nullable=False)
    repeat_days = Column(Text, nullable=False)
    deleted_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="routines")
    routine_elements = relationship(
        "RoutineElement",
        back_populates="routine",
        order_by="RoutineElement.order.asc()",
        cascade="all, delete",
    )

    def repeat_days_to_list(self):
        return [int(day) for day in self.repeat_days]

    @staticmethod
    def repeat_days_to_string(repeat_days):
        return "".join([str(day) for day in repeat_days])


class RoutineElement(Base):
    __tablename__ = "routine_element"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
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

    routine = relationship("Routine", back_populates="routine_elements")
    routine_logs = relationship(
        "RoutineLog",
        back_populates="routine_element",
        cascade="all, delete",
        lazy="dynamic",
    )


class RoutineLog(Base):
    __tablename__ = "routine_log"

    id = Column(Integer, primary_key=True, autoincrement=True)

    duration_minutes = Column(Integer)
    completed_at = Column(TIMESTAMP, default=func.now())
    is_skipped = Column(Integer, default=0)

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

    routine_element = relationship(
        "RoutineElement", back_populates="routine_logs"
    )
