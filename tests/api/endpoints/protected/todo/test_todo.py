from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import Todo
from app.schemas.todo import TodoDetail, TodoBase, TodoOrderUpdateInput


def test_get_todo(client: TestClient, add_todo: Todo, access_token: str):
    response = client.get(
        f"/todo/{add_todo.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = TodoDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data.id == add_todo.id
    assert response_data.title == add_todo.title
    assert response_data.content == add_todo.content


def test_create_todo(
    client: TestClient, session: Session, todo: TodoBase, access_token: str
):
    response = client.post(
        "/todo/create",
        json=todo.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = TodoDetail(**response.json().get("data"))

    assert response.status_code == 201

    assert response_data.title == todo.title
    assert response_data.content == todo.content

    assert session.query(Todo).filter(Todo.id == response_data.id).first()


def test_update_todo(
    client: TestClient, session: Session, add_todo: Todo, access_token: str
):
    request_data = TodoBase.from_orm(add_todo)

    request_data.title = "Updated title"
    request_data.content = "Updated content"

    response = client.put(
        f"/todo/{add_todo.id}",
        json=request_data.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = TodoDetail(**response.json().get("data"))

    assert response.status_code == 200
    assert TodoBase.from_orm(response_data) == TodoBase(**request_data.dict())

    assert (
        session.query(Todo)
        .filter(Todo.id == add_todo.id)
        .filter(Todo.title == request_data.title)
        .filter(Todo.content == request_data.content)
        .first()
    )


def test_delete_todo(
    client: TestClient, session: Session, add_todo: Todo, access_token: str
):
    response = client.delete(
        f"/todo/{add_todo.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204

    assert session.query(Todo).filter(Todo.id == add_todo.id).first() is None


def test_update_todo_list_order(
    client: TestClient,
    session: Session,
    access_token: str,
    add_todo_list: List[Todo],
    todo_order_update_data: TodoOrderUpdateInput,
):
    response = client.put(
        "/todo/order",
        json=todo_order_update_data.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204

    assert (
        session.query(Todo)
        .filter(Todo.id == add_todo_list[0].id)
        .first()
        .order
        == 3
    )
    assert (
        session.query(Todo)
        .filter(Todo.id == add_todo_list[1].id)
        .first()
        .order
        == 1
    )
    assert (
        session.query(Todo)
        .filter(Todo.id == add_todo_list[2].id)
        .first()
        .order
        == 2
    )
