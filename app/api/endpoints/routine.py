from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.dao import get_routine_dao
from app.dao.routine_dao import RoutineDAO
from app.database.db import get_db
from app.models.models import User
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
    db: Session = Depends(get_db),
    repository: RoutineRepository = Depends(get_routine_repository),
    user: User = Depends(get_current_user),
):
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
def get_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    dao: RoutineDAO = Depends(get_routine_dao),
):
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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    dao: RoutineDAO = Depends(get_routine_dao),
):
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
    user: User = Depends(get_current_user),
):
    routine = repository.update_routine(data)

    return Response(
        data=RoutineDetail.from_routine(routine, routine.routine_elements),
        message="Routine updated successfully",
        status_code=status.HTTP_200_OK,
    )
