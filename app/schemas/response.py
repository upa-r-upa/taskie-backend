from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    message: str = ""


class InnerErrorResponse(BaseModel):
    location: list[str]
    error_type: str | None = None


class ErrorResponse(BaseModel):
    error_type: str = None

    errors: List[InnerErrorResponse] | None = None
    message: str = ""
