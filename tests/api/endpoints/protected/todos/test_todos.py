from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import Todo
from app.schemas.todo import (
    TodoDetail,
    TodoBase,
    TodoListGetInput,
    TodoOrderUpdateInput,
)


def test_get_todo(client: TestClient, add_todo: Todo, access_token: str):
    response = client.get(
        f"/todos/{add_todo.id}",
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
        "/todos",
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
        f"/todos/{add_todo.id}",
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
        f"/todos/{add_todo.id}",
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
        "/todos/order",
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


def test_get_todo_list__valid_page_and_offset__1_page(
    client: TestClient,
    session: Session,
    access_token: str,
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=0, completed=0)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response_data = response.json().get("data")

    assert len(response_data) == 3
    assert response_data[0].get("id") == add_todo_list_with_date[0].id
    assert response_data[1].get("id") == add_todo_list_with_date[1].id
    assert response_data[2].get("id") == add_todo_list_with_date[2].id


def test_get_todo_list__valid_page_and_offset__2_page(
    client: TestClient,
    session: Session,
    access_token: str,
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=3, completed=0)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response_data = response.json().get("data")

    assert len(response_data) == 3
    assert response_data[0].get("id") == add_todo_list_with_date[3].id
    assert response_data[1].get("id") == add_todo_list_with_date[4].id
    assert response_data[2].get("id") == add_todo_list_with_date[5].id


def test_get_todo_list__valid_date_range(
    client: TestClient,
    session: Session,
    access_token: str,
    add_todo_list_with_date: List[Todo],
):

    params = TodoListGetInput(
        limit=3,
        offset=0,
        completed=0,
        start_date="2023-11-04",
        end_date="2023-11-06",
    )

    response = client.get(
        "/todos",
        params=params.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response_data = response.json().get("data")

    assert len(response_data) == 2
    assert response_data[0].get("id") == add_todo_list_with_date[4].id
    assert response_data[1].get("id") == add_todo_list_with_date[5].id


def test_get_todo_list__complete(
    client: TestClient,
    session: Session,
    access_token: str,
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=0, completed=1)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response_data = response.json().get("data")

    assert len(response_data) == 2
    assert response_data[0].get("id") == add_todo_list_with_date[8].id
    assert response_data[1].get("id") == add_todo_list_with_date[7].id
