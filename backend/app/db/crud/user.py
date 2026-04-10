from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.scheme.user import CreateUser


class UserCrud:
    @staticmethod
    async def create(db: AsyncSession, user: CreateUser) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        return await db.get(User, user_id)

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> User | None:
        return (
            await db.execute(select(User).where(User.use_name == name))
        ).scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        return (
            await db.execute(select(User).where(User.use_email == email))
        ).scalar_one_or_none()

    @staticmethod
    async def update_email_by_id(db: AsyncSession, user_id: int, new_email: str) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.use_email = new_email
            await db.flush()
        return db_user

    @staticmethod
    async def update_pw_by_id(db: AsyncSession, user_id: int, hashed_pw: str) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.use_password = hashed_pw
            await db.flush()
        return db_user

    @staticmethod
    async def delete_by_id(db: AsyncSession, user_id: int) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def exists_by_name(db: AsyncSession, name: str) -> bool:
        return (
            await db.execute(select(exists().where(User.use_name == name)))
        ).scalar()

    @staticmethod
    async def exists_by_email(db: AsyncSession, email: str) -> bool:
        return (
            await db.execute(select(exists().where(User.use_email == email)))
        ).scalar()

    @staticmethod
    async def get_by_refresh_token(db: AsyncSession, refresh_token: str):
        return (
            await db.execute(select(User).where(User.refresh_token == refresh_token))
        ).scalar_one_or_none()

    @staticmethod
    async def update_refresh_token_by_id(db: AsyncSession, user_id: int, refresh_token: str):
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = refresh_token
            await db.flush()
        return db_user
