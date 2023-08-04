import uuid
from datetime import datetime
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel, Field, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(min_length=5, max_length=16)


class UserUpdate(schemas.BaseUserUpdate):
    pass


# class UserSchema(BaseModel):
#     username: str = Field(min_length=5, max_length=16)
#     email: EmailStr
#     password: str = Field(min_length=6, max_length=10)
#
#
# class UserResponseSchema(BaseModel):
#     id: int
#     username: str
#     email: str
#     avatar: str
#
#     class Config:
#         from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TodoSchema(BaseModel):
    title: str = Field(max_length=50, min_length=3)
    description: str = Field(max_length=200, min_length=5)
    completed: Optional[bool] = False


class TodoUpdateSchema(TodoSchema):
    completed: bool


class TodoResponse(BaseModel):
    id: int = 1
    title: str
    description: str
    completed: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserRead | None

    class Config:
        from_attributes = True
