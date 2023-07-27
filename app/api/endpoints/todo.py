from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.utils import get_user_by_username
from app.database.db import get_db
from app.models.models import Todo
from app.schemas.response import Response
from app.schemas.todo import TodoBase, TodoWithID

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/{todo_id}", response_model=Response[TodoWithID], status_code=status.HTTP_200_OK
)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    username=Depends(get_current_user),
):
    user = get_user_by_username(db, username)
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    if todo.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this todo",
        )

    return Response(
        status_code=status.HTTP_200_OK,
        data=TodoWithID.from_orm(todo),
        message="Todo data retrieved successfully",
    )


@router.post(
    "/create",
    response_model=Response[TodoBase],
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    data: TodoBase,
    db: Session = Depends(get_db),
    username=Depends(get_current_user),
):
    user = get_user_by_username(db, username)

    todo = Todo(
        title=data.title,
        content=data.content,
        user_id=user.id,
    )

    try:
        db.add(todo)
        db.commit()

        return Response(
            status_code=status.HTTP_201_CREATED,
            data=TodoBase.from_orm(todo),
            message="Todo created successfully",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot create todo",
        )
