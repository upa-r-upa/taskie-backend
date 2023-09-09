from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/routine",
    tags=["routine"],
    dependencies=[Depends(get_current_user)],
)
