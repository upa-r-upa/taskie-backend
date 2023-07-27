from pydantic import BaseModel, validator


class TodoBase(BaseModel):
    title: str
    content: str = None

    class Config:
        orm_mode = True


class TodoWithID(TodoBase):
    id: int
