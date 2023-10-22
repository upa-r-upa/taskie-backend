from fastapi import HTTPException, status
from app.api.strings import TODO_DOES_NOT_EXIST_ERROR
from app.models.models import Todo

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
        content: str = None,
    ) -> Todo:
        # def sql() -> Todo:
        #     query = text(
        #         """
        #             INSERT INTO todo (
        #                 title, content, user_id,
        #                 completed, created_at, updated_at
        #                 )
        #             VALUES (
        #                 :title, :content, :user_id, 0,
        #                 datetime('now'), datetime('now')
        #                 )
        #         """
        #     )

        #     values = {
        #         "title": title,
        #         "content": content,
        #         "user_id": self.user_id,
        #     }
        #     try:
        #         self.db.execute(query, values)
        #         self.db.flush()

        #     except Exception:
        #         self.db.rollback()
        #         raise Exception("Failed to create todo")
        #     else:
        #         self.db.commit()

        #         todo_id = self.db.execute(
        #             text("SELECT last_insert_rowid()")
        #         ).scalar()

        #         return self.get_todo_by_id(todo_id=todo_id)

        todo = Todo(
            title=title,
            content=content,
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

        self.db.delete(todo)

        return None
