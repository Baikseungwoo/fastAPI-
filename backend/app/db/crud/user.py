from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, exists
from app.db.models import User
from app.db.scheme.user import CreateUser, UpdateUser

class UserCrud:

    # 이미 존재하는지 여부 확인
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


    # R
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

    # R for 관리자
    @ staticmethod
    async def get_multi(db:AsyncSession, skip:int=0, limit:int=50):
        result=await db.execute(
            select(User).order_by(User.use_id).offset(skip).limit(limit)
        )
        return result.scalars().all()


    # C U D
    @staticmethod
    async def create(db:AsyncSession, user:CreateUser)-> User:
        db_user=User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user

    @staticmethod
    async def update_by_id(db:AsyncSession, use_id:int, user:UpdateUser)-> User | None:
        db_user=await db.get(User, use_id)
        if db_user:
            update_data=user.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
                await db.flush()
            return db_user
        return None

    @staticmethod
    async def delete_by_id(db:AsyncSession, user_id:int)-> User | None:
        db_user=await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None
    

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