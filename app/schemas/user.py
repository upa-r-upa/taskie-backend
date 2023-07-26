import re
from pydantic import BaseModel, validator


class UserData(BaseModel):
    username: str
    email: str
    grade: int
    profile_image: str | None
    nickname: str | None

    class Config:
        orm_mode = True


class UserUpdateInput(BaseModel):
    username: str
    password: str
    email: str | None
    profile_image: str | None
    nickname: str | None

    class Config:
        orm_mode = True

    @validator("username")
    def username_length(cls: "UserUpdateInput", v: str):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @validator("password")
    def password_length(cls: "UserUpdateInput", v: str):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @validator("email")
    def email_format(cls: "UserUpdateInput", v: str):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v
