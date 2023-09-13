from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.strings import SERVER_UNTRACKED_ERROR, TODO_DOES_NOT_EXIST_ERROR

from app.core.auth import get_current_user
from app.database.db import get_db
from app.models.models import Todo, User
from app.schemas.response import Response
from app.schemas.todo import TodoBase, TodoDetail

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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == user.id)
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TODO_DOES_NOT_EXIST_ERROR,
        )

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
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    todo = Todo(
        title=data.title,
        content=data.content,
        user_id=user.id,
    )

    try:
        db.add(todo)
        db.commit()

        return Response(
            status_code=status.HTTP_201_CREATED, data=TodoDetail.from_orm(todo)
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SERVER_UNTRACKED_ERROR,
        )


@router.put(
    "/{todo_id}",
    response_model=Response[TodoDetail],
    status_code=status.HTTP_200_OK,
)
def update_todo(
    todo_id: int,
    data: TodoBase,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.user_id == user.id)
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TODO_DOES_NOT_EXIST_ERROR,
        )

    todo.title = data.title
    todo.content = data.content

    try:
        db.commit()

        return Response(
            status_code=status.HTTP_200_OK, data=TodoDetail.from_orm(todo)
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SERVER_UNTRACKED_ERROR,
        )


@router.delete(
    "/{todo_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id)
        .filter(Todo.user_id == user.id)
        .first()
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TODO_DOES_NOT_EXIST_ERROR,
        )

    try:
        db.delete(todo)
        db.commit()

        return None
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SERVER_UNTRACKED_ERROR,
        )
