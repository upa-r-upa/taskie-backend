from pydantic import BaseModel, validator
from .validator import limit_must_be_valid


class ListLoadParams(BaseModel):
    limit: int = 20
    last_id: int | None = None

    @validator("limit")
    def validate_limit(cls, v):
        return limit_must_be_valid(v)
