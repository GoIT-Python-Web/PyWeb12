
from typing import Optional

from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True
