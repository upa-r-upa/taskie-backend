from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    grade = db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String(100))
    nickname = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("todos", lazy=True))


class Habit(db.Model):
    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Integer, default=0)
    start_time_minutes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = db.relationship("User", backref=db.backref("habits", lazy=True))


class HabitTodo(db.Model):
    __tablename__ = "habit_todo"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(
        db.Integer, db.ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class HabitRepeatDay(db.Model):
    __tablename__ = "habit_repeat_day"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(
        db.Integer, db.ForeignKey("habit.id", ondelete="CASCADE"), nullable=False
    )
    day = db.Column(db.Integer, nullable=False)


class Routine(db.Model):
    __tablename__ = "routine"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.Text, nullable=False, unique=True)
    start_time_minutes = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=1)

    user = db.relationship("User", backref=db.backref("routines", lazy=True))


class TodoRoutine(db.Model):
    __tablename__ = "todo_routine"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    routine_id = db.Column(
        db.Integer, db.ForeignKey("routine.id", ondelete="CASCADE"), nullable=False
    )
    todo_id = db.Column(
        db.Integer, db.ForeignKey("todo.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    duration_minutes = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class RoutineRepeatDay(db.Model):
    __tablename__ = "routine_repeat_day"

    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(
        db.Integer, db.ForeignKey("routine.id", ondelete="CASCADE"), nullable=False
    )
    day = db.Column(db.Integer, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
