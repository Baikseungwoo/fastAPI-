from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


# 공통 제조사 정보
class FactoryBase(BaseModel):
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None


# 제조사 회원가입
class CreateFactory(BaseModel):
    fac_name: str
    fac_email: EmailStr
    fac_size: str | None = None
    fac_pw: Annotated[str, Field(max_length=72)]


# 제조사 로그인
class LoginFactory(BaseModel):
    fac_email: EmailStr
    fac_pw: str


# 제조사 정보
class FactoryInDB(FactoryBase):
    fac_id: int
    fac_pw: str

    class Config:
        from_attributes = True


class ReadFactory(FactoryBase):
    fac_id: int

    class Config:
        from_attributes = True


# 이메일 수정
class UpdateFactoryEmail(BaseModel):
    old_email: EmailStr
    new_email: EmailStr


# 비밀번호 수정
class UpdateFactoryPassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8, max_length=72)]


# 제조사 정보 수정
class UpdateFactory(BaseModel):
    fac_name: str | None = None
    fac_size: str | None = None


# 계정 삭제
class DeleteFactory(BaseModel):
    fac_pw: str


# 토큰 응답
class FactoryTokenResponse(BaseModel):
    access_token: str
    token_type: str
