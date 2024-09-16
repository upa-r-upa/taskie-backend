from typing import List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import Todo
from app.schemas.todo import (
    TodoPublic,
    TodoBase,
    TodoListGetInput,
    TodoOrderUpdateInput,
)


def test_get_todo(
    client: TestClient, add_todo: Todo, access_token_headers: dict[str, str]
):
    response = client.get(
        f"/todos/{add_todo.id}",
        headers=access_token_headers,
    )

    response_data = TodoPublic(**response.json())

    assert response.status_code == 200

    assert response_data.id == add_todo.id
    assert response_data.title == add_todo.title
    assert response_data.content == add_todo.content


def test_create_todo(
    client: TestClient,
    session: Session,
    todo: TodoBase,
    access_token_headers: dict[str, str],
):
    response = client.post(
        "/todos",
        json=todo.dict(),
        headers=access_token_headers,
    )

    response_data = TodoPublic(**response.json())

    assert response.status_code == 201

    assert response_data.title == todo.title
    assert response_data.content == todo.content
    assert response_data.target_date.strftime("%Y-%m-%d") is not None

    assert session.query(Todo).filter(Todo.id == response_data.id).first()


def test_update_todo(
    client: TestClient,
    session: Session,
    add_todo: Todo,
    access_token_headers: dict[str, str],
):
    request_data = dict(
        title="Updated title",
        content="Updated content",
        target_date="2024-07-24",
    )

    response = client.put(
        f"/todos/{add_todo.id}",
        json=request_data,
        headers=access_token_headers,
    )

    response_data = TodoPublic(**response.json())

    assert response.status_code == 200
    assert response_data.title == request_data["title"]
    assert response_data.content == request_data["content"]
    assert (
        response_data.target_date.strftime("%Y-%m-%d")
        == request_data["target_date"]
    )

    assert (
        session.query(Todo)
        .filter(Todo.id == add_todo.id)
        .filter(Todo.title == request_data["title"])
        .filter(Todo.content == request_data["content"])
        .first()
        .target_date.strftime("%Y-%m-%d")
        == request_data["target_date"]
    )


def test_delete_todo(
    client: TestClient,
    session: Session,
    add_todo: Todo,
    access_token_headers: dict[str, str],
):
    response = client.delete(
        f"/todos/{add_todo.id}",
        headers=access_token_headers,
    )

    assert response.status_code == 204

    assert session.query(Todo).filter(Todo.id == add_todo.id).first() is None


def test_update_todo_list_order(
    client: TestClient,
    session: Session,
    access_token_headers: dict[str, str],
    add_todo_list: List[Todo],
    todo_order_update_data: TodoOrderUpdateInput,
):
    response = client.put(
        "/todos/order",
        json=todo_order_update_data.dict(),
        headers=access_token_headers,
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
    access_token_headers: dict[str, str],
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=0, completed=False)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 3
    assert response_data[0].get("id") == 7
    assert response_data[1].get("id") == 6
    assert response_data[2].get("id") == 5


def test_get_todo_list__valid_page_and_offset__2_page(
    client: TestClient,
    session: Session,
    access_token_headers: dict[str, str],
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=3, completed=False)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 3
    assert response_data[0].get("id") == 4
    assert response_data[1].get("id") == 3
    assert response_data[2].get("id") == 2


def test_get_todo_list__valid_date_range(
    client: TestClient,
    session: Session,
    access_token_headers: dict[str, str],
    add_todo_list_with_date: List[Todo],
):

    params = TodoListGetInput(
        limit=3,
        offset=0,
        completed=False,
        start_date="2023-11-04",
        end_date="2023-11-06",
    )

    response = client.get(
        "/todos",
        params=params.dict(),
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 3
    assert response_data[0].get("id") == 3
    assert response_data[1].get("id") == 2
    assert response_data[2].get("id") == 1


def test_get_todo_list__complete(
    client: TestClient,
    session: Session,
    access_token_headers: dict[str, str],
    add_todo_list_with_date: List[Todo],
):
    params = TodoListGetInput(limit=3, offset=0, completed=True)

    response = client.get(
        "/todos",
        params=params.dict(),
        headers=access_token_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 2
    assert response_data[0].get("id") == 9
    assert response_data[1].get("id") == 8
