from pydantic import BaseModel


class UserRequestedAdd(BaseModel):
    email: str
    password: str


class UserAdd(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: str
