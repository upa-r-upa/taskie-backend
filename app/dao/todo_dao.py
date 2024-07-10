import datetime
from operator import and_
from typing import List
from fastapi import HTTPException, status
from app.api.strings import TODO_DOES_NOT_EXIST_ERROR
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
                detail=TODO_DOES_NOT_EXIST_ERROR,
            )

        return todo

    def create_todo(
        self,
        title: str,
        order: int,
        content: str = None,
    ) -> Todo:
        todo = Todo(
            title=title,
            content=content,
            order=order,
            user_id=self.user_id,
        )

        self.db.add(todo)

        return todo

    def update_todo(
        self, todo_id: int, title: str, content: str = None
    ) -> Todo:
        todo = self.get_todo_by_id(todo_id=todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TODO_DOES_NOT_EXIST_ERROR,
            )

        todo.title = title
        todo.content = content

        return todo

    def delete_todo(self, todo_id: int) -> None:
        todo = self.get_todo_by_id(todo_id=todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TODO_DOES_NOT_EXIST_ERROR,
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
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> List[Todo]:
        query = self.db.query(Todo).filter(
            Todo.user_id == self.user_id, Todo.completed == int(completed)
        )

        if start_date and end_date:
            query = query.filter(
                and_(Todo.updated_at >= start_date, Todo.updated_at < end_date)
            )

        todo = (
            query.order_by(Todo.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return todo
