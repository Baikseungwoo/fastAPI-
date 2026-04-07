from pydantic import BaseModel, Field, EmailStr
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

# 이메일과 비번 업데이트도 UpdateUser로 묶을 수 있는지?
class UpdateEmail(BaseModel):
    old_email:str
    new_email:Annotated[str,EmailStr]

class UpdatePassword(BaseModel):
    old_password:str
    new_password:Annotated[str,Field(min_length=8, max_length=72)]    

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

class DeleteUser(BaseModel):
    password:str

# class TokenResponse(BaseModel):
#     access_token:str
#     refresh_token:str
#     token_type:str