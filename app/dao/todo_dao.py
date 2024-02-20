import datetime
from operator import and_
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import text
from app.api.strings import TODO_DOES_NOT_EXIST_ERROR
from app.models.models import Todo
from app.schemas.todo import TodoOrderUpdate

from .base import ProtectedBaseDAO


class TodoDAO(ProtectedBaseDAO):
    def get_todo_by_id(self, todo_id: int) -> Todo:
        """
        query = text(
                SELECT * FROM todo
                WHERE id = :todo_id AND user_id = :user_id
            )

        result = self.db.execute(
            query,
            {
                "todo_id": todo_id,
                "user_id": self.user_id,
            },
        )

        todo = result.fetchone()
        """

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
        # def sql():
        #     query = text(
        #         """
        #                 UPDATE todo
        #                 SET title = :title, content = :content,
        #                 updated_at = datetime('now')
        #                 WHERE id = :todo_id
        #             """
        #     )

        #     values = {
        #         "todo_id": todo_id,
        #         "title": title,
        #         "content": content,
        #     }

        #     self.db.execute(query, values)
        #     self.db.flush()

        #     return self.get_todo_by_id(todo_id=todo_id)

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
        # def sql():
        #     query = text(
        #         """
        #                 DELETE FROM todo
        #                 WHERE id = :todo_id
        #         """
        #     )

        #     values = {"todo_id": todo_id}

        #     self.db.execute(query, values)
        #     self.db.flush()

        #     return None

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
            # UPDATE todo SET order = :order WHERE id = :todo_id
            target_todo = self.get_todo_by_id(todo_id=todo.id)

            target_todo.order = todo.order

        return None

    def get_todo_list(
        self,
        limit: int,
        offset: int,
        completed: int = 0,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> List[Todo]:
        # if start_date and end_date:
        #     query = text(
        #         """
        #                 SELECT * FROM todo
        #                 WHERE user_id = :user_id AND completed = :completed
        #                 AND updated_at BETWEEN :start_date AND :end_date
        #                 ORDER BY updated_at DESC
        #                 LIMIT :limit OFFSET :offset
        #             """
        #     )

        # result = self.db.execute(
        #     query,
        #     {
        #         "user_id": self.user_id,
        #         "completed": completed,
        #         "limit": limit,
        #         "offset": offset,
        #         "start_date": start_date,
        #         "end_date": end_date,
        #     },
        # )

        # list = result.fetchall()

        query = self.db.query(Todo).filter(
            Todo.user_id == self.user_id, Todo.completed == completed
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
