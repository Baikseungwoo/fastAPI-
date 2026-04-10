from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt_handle import (
    create_access_token,
    create_refresh_token,
    get_pw_hash,
    verify_pw,
)
from app.db.crud import UserCrud
from app.db.models import User
from app.db.scheme.user import CreateUser, LoginUser


class UserService:
    @staticmethod
    async def signup(db: AsyncSession, user: CreateUser):
        if await UserCrud.exists_by_name(db, user.use_name):
            raise HTTPException(status_code=400, detail="name already in use")
        if await UserCrud.exists_by_email(db, user.use_email):
            raise HTTPException(status_code=400, detail="email already in use")

        hash_pw = get_pw_hash(user.use_password)
        user_create = CreateUser(
            use_name=user.use_name,
            use_password=hash_pw,
            use_email=user.use_email,
        )

        try:
            db_user = await UserCrud.create(db, user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="failed to create user")

    @staticmethod
    async def login(db: AsyncSession, user: LoginUser):
        db_user = await UserCrud.get_by_name(db, user.use_name)
        if not db_user or not verify_pw(user.use_password, db_user.use_password):
            raise HTTPException(status_code=401, detail="invalid credentials")

        user_id = db_user.use_id
        refresh_token = create_refresh_token(user_id)
        access_token = create_access_token(user_id)

        await UserCrud.update_refresh_token_by_id(db, user_id, refresh_token)
        await db.commit()
        await db.refresh(db_user)

        return db_user, access_token, refresh_token

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User:
        db_user = await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")
        return db_user

    @staticmethod
    async def update_email(db: AsyncSession, user_id: int, old_email: str, new_email: str):
        db_user = await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")

        if db_user.use_email != old_email:
            raise HTTPException(status_code=400, detail="old email does not match")

        if await UserCrud.get_by_email(db, new_email):
            raise HTTPException(status_code=400, detail="email already in use")

        try:
            updated_user = await UserCrud.update_email_by_id(db, user_id, new_email)
            await db.commit()
            await db.refresh(updated_user)
            return updated_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="failed to update email")

    @staticmethod
    async def update_password(db: AsyncSession, user_id: int, old_password: str, new_password: str):
        db_user = await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")

        if not verify_pw(old_password, db_user.use_password):
            raise HTTPException(status_code=401, detail="password does not match")

        hashed_pw = get_pw_hash(new_password)

        try:
            updated_user = await UserCrud.update_pw_by_id(db, user_id, hashed_pw)
            await db.commit()
            await db.refresh(updated_user)
            return updated_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="failed to update password")

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int, password: str):
        db_user = await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")

        if not verify_pw(password, db_user.use_password):
            raise HTTPException(status_code=401, detail="password does not match")

        try:
            await UserCrud.delete_by_id(db, user_id)
            await db.commit()
            return "account deleted"
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="failed to delete account")
