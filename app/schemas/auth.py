import re
from pydantic import BaseModel, validator


class SignupInput(BaseModel):
    username: str
    password: str
    password_confirm: str
    email: str
    grade: int = 0
    profile_image: str | None = None
    nickname: str | None = None

    @validator("password_confirm")
    def password_match(cls: "SignupInput", v: str, values: dict[str, str]):
        if "password" in values and v != values["password"]:
            raise ValueError("Password does not match")
        return v

    @validator("username")
    def username_length(cls: "SignupInput", v: str):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @validator("password")
    def password_length(cls: "SignupInput", v: str):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @validator("email")
    def email_format(cls: "SignupInput", v: str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v


class SignupOutput(BaseModel):
    username: str
    email: str
    grade: int
    profile_image: str | None
    nickname: str | None

    class Config:
        orm_mode = True


class LoginInput(BaseModel):
    username: str
    password: str


class LoginOutput(BaseModel):
    access_token: str


class RefreshOutput(BaseModel):
    access_token: str


class UserBase(BaseModel):
    username: str
    password: str
    email: str
    grade: int = 0
    profile_image: str | None = None
    nickname: str | None = None

    class Config:
        orm_mode = True
