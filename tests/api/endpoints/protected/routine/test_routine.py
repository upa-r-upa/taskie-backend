from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineElement

from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineUpdateInput,
)


def test_create_routine(
    client: TestClient,
    session: Session,
    routine_data: RoutineCreateInput,
    access_token: str,
):
    response = client.post(
        "/routine/create",
        json=routine_data.dict(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 201

    assert response_data.title == routine_data.title
    assert response_data.start_time_minutes == routine_data.start_time_minutes
    assert response_data.repeat_days == routine_data.repeat_days

    assert len(response_data.routine_elements) == len(
        routine_data.routine_elements
    )

    for routine_item, todo_item in zip(
        response_data.routine_elements, routine_data.routine_elements
    ):
        assert routine_item.title == todo_item.title
        assert routine_item.duration_minutes == todo_item.duration_minutes

    assert session.query(Routine).count() == 1
    assert session.query(RoutineElement).count() == len(
        routine_data.routine_elements
    )


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


def test_update_routine_full_update(
    client: TestClient,
    access_token: str,
    add_routine: RoutineDetail,
    update_routine_all_data: RoutineUpdateInput,
):
    response = client.put(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_routine_all_data.dict(),
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data.title == update_routine_all_data.title
    assert (
        response_data.start_time_minutes
        == update_routine_all_data.start_time_minutes
    )
    assert response_data.repeat_days == update_routine_all_data.repeat_days
    assert (
        response_data.routine_elements[0].title
        == update_routine_all_data.routine_elements[0].title
    )
    assert (
        response_data.routine_elements[1].title
        == update_routine_all_data.routine_elements[1].title
    )
    assert len(response_data.routine_elements) == len(
        update_routine_all_data.routine_elements
    )


def test_update_routine_only_elements_data(
    client: TestClient,
    access_token: str,
    add_routine: RoutineDetail,
    update_routine_only_elements_data: RoutineUpdateInput,
):
    response = client.put(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_routine_only_elements_data.dict(),
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data.title == add_routine.title
    assert response_data.start_time_minutes == add_routine.start_time_minutes

    assert len(response_data.routine_elements) == len(
        update_routine_only_elements_data.routine_elements
    )

    assert (
        response_data.routine_elements[0].title
        == update_routine_only_elements_data.routine_elements[0].title
    )
    assert (
        response_data.routine_elements[1].title
        == update_routine_only_elements_data.routine_elements[1].title
    )
    assert (
        response_data.routine_elements[2].title
        == update_routine_only_elements_data.routine_elements[2].title
    )
    assert (
        response_data.routine_elements[3].title
        == update_routine_only_elements_data.routine_elements[3].title
    )


def test_update_routine_only_routine_data(
    client: TestClient,
    access_token: str,
    add_routine: RoutineDetail,
    update_routine_only_routine_data: RoutineUpdateInput,
):
    response = client.put(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_routine_only_routine_data.dict(),
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data.title == update_routine_only_routine_data.title
    assert (
        response_data.start_time_minutes
        == update_routine_only_routine_data.start_time_minutes
    )
    assert (
        response_data.repeat_days
        == update_routine_only_routine_data.repeat_days
    )

    for routine_item, todo_item in zip(
        response_data.routine_elements, add_routine.routine_elements
    ):
        assert routine_item.title == todo_item.title
        assert routine_item.duration_minutes == todo_item.duration_minutes


def test_update_routine_empty_routine_elements(
    client: TestClient,
    access_token: str,
    add_routine: RoutineDetail,
    update_routine_empty_routine_elements: RoutineUpdateInput,
):
    response = client.put(
        "/routine/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_routine_empty_routine_elements.dict(),
    )

    response_data = RoutineDetail(**response.json().get("data"))

    assert response.status_code == 200

    assert response_data.title == add_routine.title
    assert response_data.start_time_minutes == add_routine.start_time_minutes
    assert response_data.repeat_days == add_routine.repeat_days

    assert len(response_data.routine_elements) == 0
