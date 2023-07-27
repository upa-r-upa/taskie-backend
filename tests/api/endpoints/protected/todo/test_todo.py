from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.models import Todo
from app.schemas.todo import TodoWithID, TodoBase


def test_get_todo(client: TestClient, add_todo: Todo, access_token: str):
    response = client.get(
        f"/todo/{add_todo.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = TodoWithID(**response.json().get("data"))

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

    response_data = TodoWithID(**response.json().get("data"))

    assert response.status_code == 201

    assert response_data.title == todo.title
    assert response_data.content == todo.content

    assert session.query(Todo).filter(Todo.id == response_data.id).first()
