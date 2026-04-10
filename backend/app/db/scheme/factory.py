from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class FactoryBase(BaseModel):
    fac_id: int
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None
    fac_pw: str


class CreateFactory(BaseModel):
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None
    fac_pw: Annotated[str, Field(max_length=72)]


class LoginFactory(BaseModel):
    fac_email: EmailStr
    fac_pw: str


class FactoryInDB(FactoryBase):
    class Config:
        from_attributes = True


class ReadFactory(FactoryInDB):
    pass


class UpdateFactoryEmail(BaseModel):
    old_email: EmailStr
    new_email: EmailStr


class UpdateFactoryPassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8, max_length=72)]


class UpdateFactory(BaseModel):
    fac_name: str | None = None
    fac_size: str | None = None


class DeleteFactory(BaseModel):
    fac_pw: str


class FactoryTokenResponse(BaseModel):
    access_token: str
    token_type: str


# Backward-compatible aliases for existing router imports.
FactoryCreate = CreateFactory
FactoryLogin = LoginFactory
FactoryRead = ReadFactory
FactoryToken = FactoryTokenResponse
