from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .user import router as user_router
from .todo import router as todo_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(health_router)
router.include_router(user_router)
router.include_router(todo_router)
