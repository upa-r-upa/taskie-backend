from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
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
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    todos = relationship("Todo", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    routines = relationship("Routine", back_populates="user")


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    completed = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="todos")


class Habit(Base):
    __tablename__ = "habit"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    active = Column(Integer, default=0)
    start_time_minutes = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="habits")


class HabitTodo(Base):
    __tablename__ = "habit_todo"

    id = Column(Integer, primary_key=True)
    habit_id = Column(
        Integer, ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    completed = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


class HabitRepeatDay(Base):
    __tablename__ = "habit_repeat_day"

    id = Column(Integer, primary_key=True)
    habit_id = Column(
        Integer, ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )
    day = Column(Integer, nullable=False)


class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False, unique=True)
    start_time_minutes = Column(Integer, nullable=False)
    completed = Column(Integer, default=0)
    active = Column(Integer, default=1)

    user = relationship("User", back_populates="routines")


class TodoRoutine(Base):
    __tablename__ = "todo_routine"

    id = Column(Integer, primary_key=True, autoincrement=True)
    routine_id = Column(
        Integer, ForeignKey("routine.id", ondelete="CASCADE"), nullable=False
    )
    todo_id = Column(Integer, ForeignKey("todo.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    duration_minutes = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


class RoutineRepeatDay(Base):
    __tablename__ = "routine_repeat_day"

    id = Column(Integer, primary_key=True)
    routine_id = Column(
        Integer, ForeignKey("routine.id", ondelete="CASCADE"), nullable=False
    )
    day = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
