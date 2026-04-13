from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jwt_handle import create_access_token, get_pw_hash, verify_pw
from app.db.crud.factory import FactoryCrud
from app.db.scheme import factory as factory_schema


class FactoryService:

    # 제조사 회원가입
    @staticmethod
    async def create_factory(db: AsyncSession, factory_data: factory_schema.CreateFactory):
        exists = await FactoryCrud.get_by_email(db, factory_data.fac_email)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다.",
            )

        try:
            hashed_pw = get_pw_hash(factory_data.fac_pw)

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

    # 제조사 로그인
    @staticmethod
    async def login_factory(db: AsyncSession, login_data: factory_schema.LoginFactory):
        factory = await FactoryCrud.get_by_email(db, login_data.fac_email)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        is_valid = verify_pw(login_data.fac_pw, factory.fac_pw)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        access_token = create_access_token(factory.fac_id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    # 제조사 내 정보 조회
    @staticmethod
    async def get_my_factory(db: AsyncSession, fac_id: int):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="제조사 정보를 찾을 수 없습니다.",
            )
        return factory

    # 제조사 기본 정보 수정
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
                detail="제조사 정보를 찾을 수 없습니다.",
            )

        try:
            updated = await FactoryCrud.update(db, factory, update_data)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception:
            await db.rollback()
            raise

    # 이메일 수정
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
                detail="제조사 정보를 찾을 수 없습니다.",
            )

        if factory.fac_email != email_data.old_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="기존 이메일이 일치하지 않습니다.",
            )

        exists = await FactoryCrud.get_by_email(db, email_data.new_email)
        if exists and exists.fac_id != fac_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다.",
            )

        try:
            updated = await FactoryCrud.update_email(db, factory, email_data.new_email)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception:
            await db.rollback()
            raise

    # 비밀번호 수정
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
                detail="제조사 정보를 찾을 수 없습니다.",
            )

        is_valid = verify_pw(pw_data.old_password, factory.fac_pw)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="기존 비밀번호가 일치하지 않습니다.",
            )

        try:
            hashed_pw = get_pw_hash(pw_data.new_password)
            await FactoryCrud.update_password(db, factory, hashed_pw)
            await db.commit()
            return {"message": "비밀번호가 수정되었습니다."}
        except Exception:
            await db.rollback()
            raise

    # 계정 삭제
    @staticmethod
    async def delete_factory(
        db: AsyncSession,
        fac_id: int,
        delete_data: factory_schema.DeleteFactory,
    ):
        factory = await FactoryCrud.get_by_id(db, fac_id)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="제조사 정보를 찾을 수 없습니다.",
            )

        is_valid = verify_pw(delete_data.fac_pw, factory.fac_pw)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호가 일치하지 않습니다.",
            )

        try:
            await FactoryCrud.delete(db, factory)
            await db.commit()
            return {"message": "제조사 계정이 삭제되었습니다."}
        except Exception:
            await db.rollback()
            raise
