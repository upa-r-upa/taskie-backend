from typing import List
import pytest
from sqlalchemy.orm import Session

from app.models.models import Todo, User
from app.schemas.todo import TodoBase, TodoOrderUpdateInput, TodoOrderUpdate


@pytest.fixture
def todo() -> TodoBase:
    return TodoBase(title="Test title", content="Test content", order=1)


@pytest.fixture
def todo_list() -> List[TodoBase]:
    return [
        TodoBase(title="Test title 1", content="Test content 1", order=1),
        TodoBase(title="Test title 2", content="Test content 2", order=2),
        TodoBase(title="Test title 3", content="Test content 3", order=3),
    ]


@pytest.fixture
def add_todo(todo: TodoBase, session: Session, add_user: User) -> Todo:
    todo_item = Todo(
        title=todo.title,
        content=todo.content,
        user_id=add_user.id,
        order=todo.order,
    )

    session.add(todo_item)
    session.commit()

    return todo_item


@pytest.fixture
def add_todo_list(
    todo_list: List[TodoBase], session: Session, add_user: User
) -> List[Todo]:
    todo_list_items = []

    for todo in todo_list:
        todo_item = Todo(
            title=todo.title,
            content=todo.content,
            user_id=add_user.id,
            order=todo.order,
        )

        session.add(todo_item)
        session.commit()

        todo_list_items.append(todo_item)

    return todo_list_items


@pytest.fixture
def todo_order_update_data() -> TodoOrderUpdateInput:
    return TodoOrderUpdateInput(
        todo_list=[
            TodoOrderUpdate(id=1, order=3),
            TodoOrderUpdate(id=2, order=1),
            TodoOrderUpdate(id=3, order=2),
        ]
    )
