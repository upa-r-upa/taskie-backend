from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    message: str
    status_code: int


class SimpleResponse(BaseModel):
    message: str
    status_code: int


class InnerErrorResponse(BaseModel):
    message: str
    location: list[str]


class ErrorResponse(BaseModel):
    message: str
    status_code: int
    errors: List[InnerErrorResponse] | None = None
