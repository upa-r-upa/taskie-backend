import re
from pydantic import BaseModel, validator

from app.api.errors import INVALID_EMAIL_FORMAT, VALUE_TOO_SHORT


class UserData(BaseModel):
    username: str
    email: str
    nickname: str | None

    class Config:
        orm_mode = True


class UserUpdateInput(BaseModel):
    username: str
    password: str
    email: str | None
    nickname: str | None

    class Config:
        orm_mode = True

    @validator("username")
    def username_length(cls: "UserUpdateInput", v: str):
        if len(v) < 3:
            raise ValueError(VALUE_TOO_SHORT)
        return v

    @validator("password")
    def password_length(cls: "UserUpdateInput", v: str):
        if len(v) < 6:
            raise ValueError(VALUE_TOO_SHORT)
        return v

    @validator("email")
    def email_format(cls: "UserUpdateInput", v: str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, v):
            raise ValueError(INVALID_EMAIL_FORMAT)
        return v
