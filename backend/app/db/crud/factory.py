from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.factory import Factory
from app.db.scheme import factory as factory_schema


class FactoryCrud:

    # 이메일로 제조사 조회
    @staticmethod
    async def get_by_email(db: AsyncSession, fac_email: str):
        result = await db.execute(
            select(Factory).where(Factory.fac_email == fac_email)
        )
        return result.scalar_one_or_none()

    # id로 제조사 조회
    @staticmethod
    async def get_by_id(db: AsyncSession, fac_id: int):
        result = await db.execute(
            select(Factory).where(Factory.fac_id == fac_id)
        )
        return result.scalar_one_or_none()

    # 제조사 생성
    @staticmethod
    async def create(db: AsyncSession, factory_data: factory_schema.CreateFactory):
        factory = Factory(
            fac_name=factory_data.fac_name,
            fac_email=factory_data.fac_email,
            fac_size=factory_data.fac_size,
            fac_pw=factory_data.fac_pw,
        )
        db.add(factory)
        return factory

    # 제조사 기본 정보 수정
    @staticmethod
    async def update(
        db: AsyncSession,
        factory: Factory,
        update_data: factory_schema.UpdateFactory,
    ):
        if update_data.fac_name is not None:
            factory.fac_name = update_data.fac_name

        if update_data.fac_size is not None:
            factory.fac_size = update_data.fac_size

        return factory

    # 이메일 수정
    @staticmethod
    async def update_email(db: AsyncSession, factory: Factory, new_email: str):
        factory.fac_email = new_email
        return factory

    # 비밀번호 수정
    @staticmethod
    async def update_password(db: AsyncSession, factory: Factory, new_password: str):
        factory.fac_pw = new_password
        return factory

    # 계정 삭제
    @staticmethod
    async def delete(db: AsyncSession, factory: Factory):
        await db.delete(factory)
