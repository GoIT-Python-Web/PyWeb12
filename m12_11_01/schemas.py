from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OwnerModel(BaseModel):
    email: EmailStr


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr

    class Config:
        from_attributes = True


class CatModel(BaseModel):
    nick: str = Field('Barsik', min_length=3, max_length=25)
    age: int = Field(1, ge=1, le=40)
    description: str
    vaccinated: Optional[bool] = False
    owner_id: int = Field(1, gt=0)


class CatVaccinatedModel(BaseModel):
    vaccinated: bool


class CatResponse(BaseModel):
    id: int = 1
    nick: str = 'Barsik'
    age: int = Field(1, ge=1, le=40)
    description: str
    vaccinated: bool = False
    owner: OwnerResponse

    class Config:
        from_attributes = True
