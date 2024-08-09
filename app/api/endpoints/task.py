from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.repositories import get_task_repository
from app.repositories.task_repository import TaskRepository
from app.schemas.response import Response
from app.schemas.task import TaskGetInput, TaskPublic


router = APIRouter(
    prefix="/task",
    tags=["task"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=Response[TaskPublic],
    status_code=status.HTTP_200_OK,
    operation_id="getAllDailyTask",
)
def get_today_all_task(
    params: TaskGetInput = Depends(),
    task_repository: TaskRepository = Depends(get_task_repository),
):
    all_task = task_repository.get_all_task_by_date(date=params.date)

    return Response(data=all_task)
