from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone
from typing import Annotated

class UserBase(BaseModel):
    use_id:int
    use_name:str
    use_email:str
    use_password:str

# 회원가입
class CreateUser(BaseModel):
    use_name:str
    use_email:str
    use_password:Annotated[str,Field(max_length=72)]

# 로그인
class LoginUser(BaseModel):
    use_name:str
    use_password:str

# 사용자 정보
class UserInDB(UserBase):
    use_id:int
    joined_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

    class Config:
        from_attributes=True

class ReadUser(UserInDB):
    pass

# 이메일 수정
class UpdateEmail(BaseModel):
    old_email:str
    new_email:Annotated[str,EmailStr]

# 비밀번호 수정
class UpdatePassword(BaseModel):
    old_password:str
    new_password:Annotated[str,Field(min_length=8, max_length=72)] 

# 계정 삭제
class DeleteUser(BaseModel):
    use_password:str