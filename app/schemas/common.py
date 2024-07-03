from pydantic import BaseModel, validator
from .validator import limit_must_be_valid


class ListLoadParams(BaseModel):
    last_id: int
    limit: int = 20

    @validator("limit")
    def validate_limit(cls, v):
        return limit_must_be_valid(v)
