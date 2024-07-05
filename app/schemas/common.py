from fastapi.params import Query
from pydantic import BaseModel


class ListLoadParams(BaseModel):
    limit: int | None = Query(30, ge=1, le=100)
    last_id: int | None = Query(None, ge=1)
