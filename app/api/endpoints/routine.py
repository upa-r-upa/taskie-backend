from contextlib import contextmanager
from fastapi import APIRouter, Depends, status
from app.core.auth import get_current_user
from app.dao import get_routine_dao
from app.dao.routine_dao import RoutineDAO
from app.database.db import tx_manager
from app.repositories import get_routine_repository
from app.repositories.routine_repository import RoutineRepository
from app.schemas.response import Response
from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineUpdateInput,
)

router = APIRouter(
    prefix="/routine",
    tags=["routine"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/create",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_201_CREATED,
)
def create_routine(
    data: RoutineCreateInput,
    repository: RoutineRepository = Depends(get_routine_repository),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        routine = repository.create_routine(data)

    return Response(
        data=routine,
        message="Routine created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
)
def get_routine(routine_id: int, dao: RoutineDAO = Depends(get_routine_dao)):
    routine = dao.get_routine_with_elements_by_id(routine_id)

    response = Response(
        data=RoutineDetail.from_routine(routine, routine.routine_elements),
        message="Routine retrieved successfully",
        status_code=status.HTTP_200_OK,
    )

    return response


@router.delete(
    "/{routine_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_routine(
    routine_id: int,
    dao: RoutineDAO = Depends(get_routine_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        dao.soft_delete_routine(routine_id)

    return None


@router.put(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
)
def update_routine(
    routine_id: int,
    data: RoutineUpdateInput,
    repository: RoutineRepository = Depends(get_routine_repository),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        routine = repository.update_routine(
            routine_id=routine_id, routine=data
        )

    return Response(
        data=RoutineDetail.from_routine(routine, routine.routine_elements),
        message="Routine updated successfully",
        status_code=status.HTTP_200_OK,
    )
