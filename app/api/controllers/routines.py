from contextlib import contextmanager
from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user

from ..dao import get_routine_dao, get_routine_log_dao
from ..repositories import get_routine_repository
from ..repositories.routine_repository import RoutineRepository

from ..dao.routine_dao import RoutineDAO
from ..dao.routine_log_dao import RoutineLogDAO

from app.database.db import tx_manager
from app.schemas.response import Response
from app.schemas.routine import (
    RoutineCreateInput,
    RoutineDetail,
    RoutineLogPutInput,
    RoutineUpdateInput,
)

router = APIRouter(
    prefix="/routines",
    tags=["routines"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_201_CREATED,
    operation_id="createRoutine",
)
def create_routine(
    data: RoutineCreateInput,
    repository: RoutineRepository = Depends(get_routine_repository),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        routine = repository.create_routine(data)

    return Response(data=routine)


@router.get(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
    operation_id="getRoutine",
)
def get_routine(routine_id: int, dao: RoutineDAO = Depends(get_routine_dao)):
    routine = dao.get_routine_with_elements_by_id(routine_id)

    response = Response(
        data=RoutineDetail.from_routine(routine, routine.routine_elements)
    )

    return response


@router.delete(
    "/{routine_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteRoutine",
)
def delete_routine(
    routine_id: int,
    dao: RoutineDAO = Depends(get_routine_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        dao.delete_routine(routine_id)

    return None


@router.put(
    "/log/{routine_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="putRoutineLog",
)
def put_routine_log(
    routine_id: int,
    data: RoutineLogPutInput,
    routine_log_dao: RoutineLogDAO = Depends(get_routine_log_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        routine_log_dao.put_logs(routine_id=routine_id, logs=data.logs)

    return None


@router.put(
    "/{routine_id}",
    response_model=Response[RoutineDetail],
    status_code=status.HTTP_200_OK,
    operation_id="updateRoutine",
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
        data=RoutineDetail.from_routine(routine, routine.routine_elements)
    )
