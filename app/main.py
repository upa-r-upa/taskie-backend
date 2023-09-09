import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.schemas.response import ErrorResponse
from app.api.error_handlers import validation_exception_handler

app = FastAPI(
    title="Taskie backend",
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)


# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:8080",
    # 필요한 경우 추가적인 origin을 여기에 나열합니다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

validation_exception_handler(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
