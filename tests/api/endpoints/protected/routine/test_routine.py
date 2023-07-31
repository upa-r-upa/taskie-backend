from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import Routine, RoutineRepeatDay, Todo, TodoRoutine

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

    assert len(response_data.todo_items) == len(routine.todo_items)

    for routine_item, todo_item in zip(response_data.todo_items, routine.todo_items):
        assert routine_item.title == todo_item.title
        assert routine_item.duration_minutes == todo_item.duration_minutes

    assert session.query(Routine).count() == 1
    assert session.query(Todo).count() == len(routine.todo_items)
    assert session.query(TodoRoutine).count() == len(routine.todo_items)
    assert session.query(RoutineRepeatDay).count() == len(routine.repeat_days)
