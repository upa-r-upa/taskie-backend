from contextlib import contextmanager
from typing import List
from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.database.db import tx_manager
from app.repositories import get_habit_repository
from app.repositories.habit_repository import HabitRepository
from app.schemas.habit import (
    HabitCreateInput,
    HabitDetail,
    HabitListGetParams,
    HabitWithLog,
)
from app.schemas.response import Response

router = APIRouter(
    prefix="/habits", tags=["habits"], dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    response_model=Response[HabitDetail],
    status_code=status.HTTP_201_CREATED,
    operation_id="createHabit",
)
def create_habit(
    data: HabitCreateInput,
    repository: HabitRepository = Depends(get_habit_repository),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        habit = repository.create_habit(data)

    return Response(data=HabitDetail.from_orm(habit))


@router.get(
    "",
    response_model=Response[List[HabitWithLog]],
    status_code=status.HTTP_200_OK,
    operation_id="getHabitList",
)
def get_habits(
    params: HabitListGetParams = Depends(),
    repository: HabitRepository = Depends(get_habit_repository),
):
    habits = repository.get_habits(**params.dict())

    return Response(data=habits)
