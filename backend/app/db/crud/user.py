from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, exists
from app.db.models import User
from app.db.scheme.user import CreateUser,LoginUser,ReadUser
from typing import Optional

class UserCrud:

    # 회원가입
    @staticmethod
    async def create(db:AsyncSession, user:CreateUser)-> User:
        db_user=User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user
    
    # 로그인 / 사용자 정보 조회
    @staticmethod
    async def get_by_name(db:AsyncSession, name:str)-> User:    
        return (await db.execute(
            select(User).filter(User.use_name==name)
        )).scalar_one_or_none()

    # 이메일 재설정
    @staticmethod
    async def update_email_by_id(db:AsyncSession, user_id:int, new_email:str)-> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            db_user.use_email=new_email
            await db.flush()
        return db_user

    # 비밀번호 재설정
    @staticmethod
    async def update_pw_by_id(db:AsyncSession, user_id:int, hashed_pw:str)-> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            db_user.use_password=hashed_pw
            await db.flush()
        return db_user

    # 계정 삭제
    @staticmethod
    async def delete_by_id(db:AsyncSession, user_id:int)-> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None

    # 닉네임 중복 검사
    @staticmethod
    async def exists_by_name(db:AsyncSession, name:str)-> bool:
        return (await db.execute(
            select(exists().where(User.use_name==name))
        )).scalar()
    
    # 이메일 중복 검사
    @staticmethod
    async def exists_by_email(db:AsyncSession, email:str)-> bool:
        return (await db.execute(
            select(exists().where(User.use_email==email))
        )).scalar()
    
    # 토큰
    @staticmethod
    async def get_by_refresh_token(db:AsyncSession, refresh_token:str):
        return (await db.execute(
            select(User).where(User.refresh_token==refresh_token)
        )).scalar_one_or_none()

    @staticmethod
    async def update_refresh_token_by_id(
        db:AsyncSession, user_id:int, refresh_token:str):
        
        db_user=await db.get(User, user_id)
        if db_user:
            db_user.refresh_token=refresh_token
            await db.flush()
        return db_user