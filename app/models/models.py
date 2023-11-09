from datetime import datetime
from pydantic import validator
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
    password = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    grade = Column(Integer, nullable=False)
    profile_image = Column(String(100))
    nickname = Column(String(50))
    created_at = Column(TIMESTAMP, default=func.now())

    todos = relationship("Todo", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    routines = relationship("Routine", back_populates="user")
    routine_elements = relationship("RoutineElement", back_populates="user")


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    completed = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now())
    order = Column(Integer, nullable=False)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="todos")


class Habit(Base):
    __tablename__ = "habit"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    start_time_minutes = Column(Integer, nullable=False)
    repeat_days = Column(Text, nullable=False)
    active = Column(Integer, default=0)
    deleted_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="habits")
    habit_logs = relationship("HabitLog", back_populates="habit")


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
    )

    @validator("repeat_days")
    def validate_repeat_days(cls, v):
        if len(v) == 0:
            raise ValueError("repeat_days must not be empty")
        for day in v:
            if day not in range(1, 8):
                raise ValueError(
                    "repeat_days must be a list of integers between 1 and 7"
                )
        return v

    @validator("start_time_minutes")
    def validate_start_time_minutes(cls, v):
        if v < 0 or v >= 1440:
            raise ValueError("start_time_minutes must be between 0 and 1439")
        return v

    @validator("routine_elements")
    def validate_routine_elements(cls, v):
        for item in v:
            if item.duration_minutes < 0:
                raise ValueError("duration_minutes must be positive")
            elif item.duration_minutes > 1440:
                raise ValueError("duration_minutes must be less than 1440")
        return v

    @validator("routine_elements")
    def validate_routine_elements_order(cls, v):
        order_list = []
        for item in v:
            order_list.append(item.order)
        order_list.sort()
        for i in range(len(order_list)):
            if order_list[i] != i + 1:
                raise ValueError("routine_elements order must be 1, 2, 3, ...")
        return v

    @validator("title")
    def validate_title(cls, v):
        if len(v) == 0:
            raise ValueError("title must not be empty")
        elif len(v) > 255:
            raise ValueError("title must be less than 255 characters")
        return v

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

    user = relationship("User", back_populates="routine_elements")
    routine = relationship("Routine", back_populates="routine_elements")
    routine_logs = relationship("RoutineLog", back_populates="routine_element")


class RoutineLog(Base):
    __tablename__ = "routine_log"

    id = Column(Integer, primary_key=True, autoincrement=True)

    completed_at = Column(TIMESTAMP, default=func.now())

    routine_element_id = Column(
        Integer, ForeignKey("routine_element.id"), nullable=False
    )

    routine_element = relationship(
        "RoutineElement", back_populates="routine_logs"
    )
