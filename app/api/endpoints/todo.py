from contextlib import contextmanager
from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user
from app.dao import get_todo_dao
from app.dao.todo_dao import TodoDAO
from app.database.db import tx_manager
from app.schemas.response import Response
from app.schemas.todo import (
    TodoBase,
    TodoDetail,
    TodoOrderUpdateInput,
    TodoUpdateInput,
)

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/{todo_id}",
    response_model=Response[TodoDetail],
    status_code=status.HTTP_200_OK,
)
def get_todo(
    todo_id: int,
    dao: TodoDAO = Depends(get_todo_dao),
):
    todo = dao.get_todo_by_id(todo_id=todo_id)

    return Response(
        status_code=status.HTTP_200_OK, data=TodoDetail.from_orm(todo)
    )


@router.post(
    "/create",
    response_model=Response[TodoDetail],
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    data: TodoBase,
    dao: TodoDAO = Depends(get_todo_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        todo = dao.create_todo(
            title=data.title,
            content=data.content,
            order=data.order,
        )

    return Response(
        status_code=status.HTTP_201_CREATED, data=TodoDetail.from_orm(todo)
    )


@router.put(
    "/order",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_todo_list_order(
    data: TodoOrderUpdateInput,
    dao: TodoDAO = Depends(get_todo_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        dao.update_todo_list_order(
            todo_list=data.todo_list,
        )

    return None


@router.put(
    "/{todo_id}",
    response_model=Response[TodoDetail],
    status_code=status.HTTP_200_OK,
)
def update_todo(
    todo_id: int,
    data: TodoUpdateInput,
    todo_dao: TodoDAO = Depends(get_todo_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        todo = todo_dao.update_todo(
            todo_id=todo_id,
            title=data.title,
            content=data.content,
        )

    return Response(
        status_code=status.HTTP_200_OK, data=TodoDetail.from_orm(todo)
    )


@router.delete(
    "/{todo_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(
    todo_id: int,
    todo_dao: TodoDAO = Depends(get_todo_dao),
    tx_manager: contextmanager = Depends(tx_manager),
):
    with tx_manager:
        todo_dao.delete_todo(
            todo_id=todo_id,
        )

    return None
