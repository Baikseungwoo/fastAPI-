from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, get_password_hash, verify_password
from app.db.crud.factory import FactoryCrud
from app.db.scheme import factory as factory_schema


class FactoryService:
    @staticmethod
    async def create_factory(db: AsyncSession, factory_data: factory_schema.CreateFactory):
        exists = await FactoryCrud.get_by_email(db, factory_data.fac_email)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="email already in use",
            )

        try:
            hashed_pw = await get_password_hash(factory_data.fac_pw)
            create_data = factory_schema.CreateFactory(
                fac_name=factory_data.fac_name,
                fac_email=factory_data.fac_email,
                fac_size=factory_data.fac_size,
                fac_pw=hashed_pw,
            )

            factory = await FactoryCrud.create(db, create_data)
            await db.commit()
            await db.refresh(factory)
            return factory
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def login_factory(db: AsyncSession, login_data: factory_schema.LoginFactory):
        factory = await FactoryCrud.get_by_email(db, login_data.fac_email)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid email or password",
            )

        is_valid = await verify_password(login_data.fac_pw, factory.fac_pw)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid email or password",
            )

        access_token = create_access_token(
            data={"sub": str(factory.fac_id), "role": "factory"}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_my_factory(db: AsyncSession, fac_id: int):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="factory not found",
            )
        return factory

    @staticmethod
    async def update_factory(
        db: AsyncSession,
        fac_id: int,
        update_data: factory_schema.UpdateFactory,
    ):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="factory not found",
            )

        try:
            updated = await FactoryCrud.update(db, factory, update_data)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def update_factory_email(
        db: AsyncSession,
        fac_id: int,
        email_data: factory_schema.UpdateFactoryEmail,
    ):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="factory not found",
            )

        if factory.fac_email != email_data.old_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="old email does not match",
            )

        exists = await FactoryCrud.get_by_email(db, email_data.new_email)
        if exists and exists.fac_id != fac_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="email already in use",
            )

        try:
            updated = await FactoryCrud.update_email(db, factory, email_data.new_email)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def update_factory_password(
        db: AsyncSession,
        fac_id: int,
        pw_data: factory_schema.UpdateFactoryPassword,
    ):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="factory not found",
            )

        is_valid = await verify_password(pw_data.old_password, factory.fac_pw)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password does not match",
            )

        try:
            hashed_pw = await get_password_hash(pw_data.new_password)
            await FactoryCrud.update_password(db, factory, hashed_pw)
            await db.commit()
            return {"message": "password updated"}
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def delete_factory(
        db: AsyncSession,
        fac_id: int,
        delete_data: factory_schema.DeleteFactory | None = None,
    ):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="factory not found",
            )

        if delete_data is not None:
            is_valid = await verify_password(delete_data.fac_pw, factory.fac_pw)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="password does not match",
                )

        try:
            await FactoryCrud.delete(db, factory)
            await db.commit()
            return {"message": "factory account deleted"}
        except Exception:
            await db.rollback()
            raise
