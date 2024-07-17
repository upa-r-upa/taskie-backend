from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.database.db import initialize_database
from app.schemas.response import ErrorResponse
from app.api.error_handlers import validation_exception_handler

app = FastAPI(
    title="Taskie backend",
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)


@app.on_event("startup")
async def startup_event():
    initialize_database()


# CORS 설정
origins = ["http://localhost:5173", "https://taskie.upa-r-upa.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

validation_exception_handler(app)
