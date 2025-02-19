from datetime import datetime
from typing import List
import pytest
from sqlalchemy.orm import Session

from app.models.models import Todo, User
from app.schemas.todo import TodoBase, TodoOrderUpdateInput, TodoOrderUpdate


@pytest.fixture
def todo() -> TodoBase:
    return TodoBase(
        title="Test title",
        content="Test content",
        order=1,
        target_date=datetime(2024, 11, 11, 0, 0, 0),
    )


@pytest.fixture
def todo_list() -> List[TodoBase]:
    return [
        TodoBase(
            title="Test title 1",
            content="Test content 1",
            order=1,
            target_date=datetime(2024, 11, 11, 0, 0, 0),
        ),
        TodoBase(
            title="Test title 2",
            content="Test content 2",
            order=2,
            target_date=datetime(2024, 11, 11, 0, 0, 0),
        ),
        TodoBase(
            title="Test title 3",
            content="Test content 3",
            order=3,
            target_date=datetime(2024, 11, 11, 0, 0, 0),
        ),
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


@pytest.fixture
def todo_list_with_date() -> List[Todo]:
    return [
        Todo(
            title="Test title 1",
            content="Test content 1",
            order=1,
            updated_at=datetime(2024, 11, 4, 0, 0, 0),
            target_date=datetime(2024, 11, 4, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 2",
            content="Test content 2",
            order=2,
            updated_at=datetime(2024, 11, 5, 0, 0, 0),
            target_date=datetime(2024, 11, 5, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 3",
            content="Test content 3",
            order=3,
            updated_at=datetime(2024, 11, 6, 0, 0, 0),
            target_date=datetime(2024, 11, 6, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 4",
            content="Test content 4",
            order=4,
            updated_at=datetime(2024, 11, 12, 0, 0, 0),
            target_date=datetime(2024, 11, 12, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 5",
            content="Test content 5",
            order=5,
            updated_at=datetime(2024, 11, 13, 0, 0, 0),
            target_date=datetime(2024, 11, 13, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 6",
            content="Test content 6",
            order=6,
            updated_at=datetime(2024, 11, 14, 0, 0, 0),
            target_date=datetime(2024, 11, 14, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 7",
            content="Test content 7",
            order=7,
            updated_at=datetime(2024, 11, 15, 0, 0, 0),
            target_date=datetime(2024, 11, 15, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 8",
            content="Test content 8",
            order=8,
            completed_at=datetime(2024, 11, 16, 0, 0, 0),
            updated_at=datetime(2024, 11, 16, 0, 0, 0),
            target_date=datetime(2024, 11, 16, 0, 0, 0),
            user_id=1,
        ),
        Todo(
            title="Test title 9",
            content="Test content 9",
            order=9,
            completed_at=datetime(2024, 11, 17, 0, 0, 0),
            updated_at=datetime(2024, 11, 17, 0, 0, 0),
            target_date=datetime(2024, 11, 17, 0, 0, 0),
            user_id=1,
        ),
    ]


@pytest.fixture
def add_todo_list_with_date(
    todo_list_with_date: List[Todo], session: Session, add_user: User
) -> List[Todo]:
    session.add_all(todo_list_with_date)
    session.commit()

    return todo_list_with_date
