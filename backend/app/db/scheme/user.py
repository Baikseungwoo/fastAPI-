from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Annotated

class UserBase(BaseModel):
    name:str
    email:str
    password:str

class CreateUser(BaseModel):
    name:str
    email:str
    password:Annotated[str,Field(max_length=72)]

class UpdateUser(BaseModel):
    email:str
    password:Annotated[str,Field(max_length=72)]

class LoginUser(BaseModel):
    name:str | None = None
    email:str | None = None
    password:str | None = None

class UserInDB(UserBase):
    user_id:int
    joined_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    class Config:
        from_attributes=True

class ReadUser(UserInDB):
    pass