from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineElement

from app.schemas.routine import RoutineCreateInput, RoutineDetail


def test_create_routine(
    client: TestClient,
    session: Session,
    routine: RoutineCreateInput,
    access_token: str,
):
    response = client.post(
        "/routine/create",
        json=routine.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 201

    assert response_data.title == routine.title
    assert response_data.start_time_minutes == routine.start_time_minutes
    assert response_data.repeat_days == routine.repeat_days

    assert len(response_data.routine_elements) == len(routine.routine_elements)

    for routine_item, todo_item in zip(
        response_data.routine_elements, routine.routine_elements
    ):
        assert routine_item.title == todo_item.title
        assert routine_item.duration_minutes == todo_item.duration_minutes
        assert routine_item.order == todo_item.order

    assert session.query(Routine).count() == 1
    assert session.query(RoutineElement).count() == len(
        routine.routine_elements)


def test_get_routine_valid_id(
    client: TestClient, access_token: str, add_routine: RoutineDetail
):
    response = client.get(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data == add_routine


def test_get_routine_invalid_id(
    client: TestClient,
    access_token: str,
):
    response = client.get(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404


def test_delete_routine_valid_id(
    client: TestClient,
    access_token: str,
    session: Session,
    add_routine: RoutineDetail,
):
    response = client.delete(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204

    assert session.query(Routine).first().deleted_at is not None


def test_delete_routine_invalid_id(
    client: TestClient,
    access_token: str,
):
    response = client.delete(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
