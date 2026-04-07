from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, exists
from app.db.models import User
from app.db.scheme.user import CreateUser

class UserCrud:

    # 회원가입
    @staticmethod
    async def create(db:AsyncSession, user:CreateUser)-> User:
        db_user=User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user
    
    # 로그인 


    # 사용자 정보 (하나로 묶기)
    @staticmethod
    async def get_by_id(db:AsyncSession, user_id:int)-> User | None:
        result=await db.execute(select(User).filter(User.use_id==user_id))
        return result.scalar_one_or_none()
        
    @staticmethod
    async def get_by_name(db:AsyncSession, username:str)-> User | None:
        result=await db.execute(select(User).filter(User.username==username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db:AsyncSession, email:str)-> User | None:
        result=await db.execute(select(User).filter(User.email==email))
        return result.scalar_one_or_none()

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
    
    # 위의 재설정 위한 코드도 하나로 묶을 수 있는건가
    # @staticmethod
    # async def update_by_id(db:AsyncSession, use_id:int, user:UpdateUser)-> User | None:
    #     db_user=await db.get(User, use_id)
    #     if db_user:
    #         update_data=user.model_dump(exclude_unset=True)
    #         for key, value in update_data.items():
    #             setattr(db_user, key, value)
    #         await db.flush()
    #         return db_user
    #     return None

    # 계정 삭제
    @staticmethod
    async def delete_by_id(db:AsyncSession, user_id:int)-> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None

    # 중복 검사 (하나로 묶기)
    @staticmethod
    async def exists_by_email(db:AsyncSession, email:str)-> bool:
        return (await db.execute(
            select(exists().where(User.use_email==email))
        )).scalar()

    @staticmethod
    async def exists_by_name(db:AsyncSession, name:str)-> bool:
        return (await db.execute(
            select(exists().where(User.use_name==name))
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