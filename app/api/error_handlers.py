from typing import List
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.response import ErrorResponse, InnerErrorResponse


def validation_exception_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(
        request: Request, exc: HTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(message=exc.detail).dict(),
            headers=exc.headers,
        )

    def _filtered_location_list(location: List[str]) -> List[str]:
        if location and location[0] in ("body", "path", "query"):
            return location[1:]
        return location

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        details = exc.errors()
        errors = []

        if (
            len(details) == 1
            and len(details[0].get("loc", [])) == 1
            and "body" in details[0].get("loc", [])
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(message="Invalid JSON payload").dict(),
            )

        for detail in details:
            errors.append(
                InnerErrorResponse(
                    message=detail["msg"],
                    location=_filtered_location_list(detail["loc"]),
                )
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                message="Validation Error", errors=errors
            ).dict(),
        )

    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(message="Internal Server Error").dict(),
        )
