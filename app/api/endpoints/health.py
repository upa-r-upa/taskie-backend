from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
