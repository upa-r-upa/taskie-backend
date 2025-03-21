from datetime import date, datetime
from pytz import timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import asc, desc, and_, func, nullsfirst, or_
from app.api.errors import DATA_DOES_NOT_EXIST
from app.models.models import Todo
from app.schemas.todo import TodoOrderUpdate

from .base import ProtectedBaseDAO


class TodoDAO(ProtectedBaseDAO):
    def get_todo_by_id(self, todo_id: int) -> Todo:
        todo = (
            self.db.query(Todo)
            .filter(Todo.id == todo_id, Todo.user_id == self.user_id)
            .first()
        )

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DATA_DOES_NOT_EXIST,
            )

        return todo

    def create_todo(
        self,
        title: str,
        order: int,
        target_date: datetime,
        content: str = None,
    ) -> Todo:
        todo = Todo(
            title=title,
            content=content,
            order=order,
            user_id=self.user_id,
            target_date=target_date,
        )

        self.db.add(todo)

        return todo

    def check_completed_updated(
        self, completed: bool, completed_at: datetime | None
    ) -> bool:
        if (completed and not completed_at) or (
            not completed and completed_at
        ):
            return True

        return False

    def update_todo(
        self,
        todo_id: int,
        title: str,
        target_date: datetime,
        completed: bool,
        content: str = None,
    ) -> Todo:
        todo = self.get_todo_by_id(todo_id=todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DATA_DOES_NOT_EXIST,
            )

        if self.check_completed_updated(completed, todo.completed_at):
            if completed:
                todo.completed_at = datetime.now(timezone("Asia/Seoul"))
            else:
                todo.completed_at = None

        todo.title = title
        todo.content = content
        todo.target_date = target_date

        return todo

    def delete_todo(self, todo_id: int) -> None:
        todo = self.get_todo_by_id(todo_id=todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DATA_DOES_NOT_EXIST,
            )

        self.db.delete(todo)

        return None

    def update_todo_list_order(self, todo_list: List[TodoOrderUpdate]) -> None:
        for todo in todo_list:
            target_todo = self.get_todo_by_id(todo_id=todo.id)

            target_todo.order = todo.order

        return None

    def get_todo_list(
        self,
        limit: int,
        offset: int,
        completed: bool = False,
        start_date: date = None,
        end_date: date = None,
    ) -> List[Todo]:
        query = self.db.query(Todo).filter(Todo.user_id == self.user_id)

        if completed:
            query = query.filter(Todo.completed_at.is_not(None))
        else:
            query = query.filter(Todo.completed_at.is_(None))

        if start_date:
            query = query.filter(func.date(Todo.target_date) >= start_date)
        if end_date:
            query = query.filter(func.date(Todo.target_date) <= end_date)

        if completed:
            query = query.order_by(desc(Todo.completed_at))
        else:
            query = query.order_by(
                asc(Todo.target_date), asc(Todo.order), desc(Todo.updated_at)
            )

        return query.limit(limit).offset(offset).all()

    def get_todo_list_by_date(
        self,
        date: date,
    ) -> List[Todo]:
        todo = (
            self.db.query(Todo)
            .filter(
                Todo.user_id == self.user_id,
                or_(
                    func.date(Todo.target_date) == date,
                    and_(
                        Todo.target_date <= date, Todo.completed_at.is_(None)
                    ),
                    func.date(Todo.completed_at) == date,
                ),
            )
            .order_by(
                nullsfirst(desc(Todo.completed_at)),
                asc(Todo.target_date),
                desc(Todo.updated_at),
            )
            .all()
        )

        return todo
