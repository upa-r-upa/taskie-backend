import re
from pydantic import BaseModel, validator

from app.api.errors import (
    INVALID_EMAIL_FORMAT,
    PASSWORD_NOT_MATCH,
    VALUE_MUST_BE_ALPHANUM,
    VALUE_TOO_LONG,
    VALUE_TOO_SHORT,
)
from app.schemas.user import UserData

USERNAME_PATTERN = r"^[A-Za-z0-9]+$"
PASSWORD_PATTERN = r"^.+$"


class SignupInput(BaseModel):
    username: str
    password: str
    password_confirm: str
    email: str
    nickname: str | None = None

    @validator("password_confirm")
    def password_match(cls: "SignupInput", v: str, values: dict[str, str]):
        if "password" in values and v != values["password"]:
            raise ValueError(PASSWORD_NOT_MATCH)
        return v

    @validator("username")
    def username_length(cls: "SignupInput", v: str):
        if len(v) < 4:
            raise ValueError(VALUE_TOO_SHORT)
        elif len(v) > 20:
            raise ValueError(VALUE_TOO_LONG)
        elif not re.match(USERNAME_PATTERN, v):
            raise ValueError(VALUE_MUST_BE_ALPHANUM)
        return v

    @validator("password")
    def password_length(cls: "SignupInput", v: str):
        if len(v) < 6:
            raise ValueError(VALUE_TOO_SHORT)
        elif len(v) > 20:
            raise ValueError(VALUE_TOO_LONG)
        elif not re.match(PASSWORD_PATTERN, v):
            raise ValueError(VALUE_MUST_BE_ALPHANUM)
        return v

    @validator("email")
    def email_format(cls: "SignupInput", v: str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, v):
            raise ValueError(INVALID_EMAIL_FORMAT)
        elif len(v) > 100:
            raise ValueError(VALUE_TOO_LONG)
        return v


class LoginInput(BaseModel):
    username: str
    password: str


class LoginOutput(BaseModel):
    access_token: str
    user: UserData


class RefreshOutput(BaseModel):
    access_token: str
    user: UserData


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    nickname: str | None = None

    class Config:
        orm_mode = True
