from datetime import datetime
from operator import and_
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import func
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
        target_date: str,
        content: str = None,
    ) -> Todo:
        todo = Todo(
            title=title,
            content=content,
            order=order,
            user_id=self.user_id,
            target_date=datetime.strptime(target_date, "%Y-%m-%d"),
        )

        self.db.add(todo)

        return todo

    def update_todo(
        self,
        todo_id: int,
        title: str,
        target_date: str,
        content: str = None,
    ) -> Todo:
        todo = self.get_todo_by_id(todo_id=todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DATA_DOES_NOT_EXIST,
            )

        todo.title = title
        todo.content = content
        todo.target_date = datetime.strptime(target_date, "%Y-%m-%d")

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
        start_date: str = None,
        end_date: str = None,
    ) -> List[Todo]:
        query = self.db.query(Todo).filter(
            Todo.user_id == self.user_id, Todo.completed == int(completed)
        )
        start_date = (
            datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        )
        end_date = (
            datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        )

        if start_date and end_date:
            query = query.filter(
                and_(
                    Todo.target_date >= start_date,
                    Todo.target_date <= end_date,
                )
            )

        todo = (
            query.order_by(Todo.target_date.desc(), Todo.order.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return todo

    def get_todo_list_by_date(
        self,
        date: str,
    ) -> List[Todo]:
        todo = (
            self.db.query(Todo)
            .filter(
                Todo.user_id == self.user_id,
                func.date(Todo.target_date) == date,
            )
            .order_by(Todo.target_date.desc(), Todo.order.asc())
            .limit(1000)
            .all()
        )

        return todo
