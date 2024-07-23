from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from pydantic import BaseModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    data: Optional[T] = None
    message: str = ""


class ErrorResponse(BaseModel):
    error_type: str

    message: str = ""
    location: str = None
