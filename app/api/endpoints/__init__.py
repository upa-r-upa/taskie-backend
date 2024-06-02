from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .users import router as users_router
from .todos import router as todos_router
from .routines import router as routines_router
from .habits import router as habits_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(health_router)
router.include_router(users_router)
router.include_router(todos_router)
router.include_router(routines_router)
router.include_router(habits_router)
