from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product
from app.db.scheme.product import ProductCreate, ProductUpdate


class ProductCrud:

    # 상품 등록
    @staticmethod
    async def create(db: AsyncSession, fac_id: int, product_data: ProductCreate):
        product = Product(
            fac_id=fac_id,
            pro_category=product_data.pro_category,
            pro_name=product_data.pro_name,
            pro_price=product_data.pro_price,
        )
        db.add(product)
        return product

    # 상품 전체 조회
    @staticmethod
    async def get_list(db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

    # 상품 단건 조회
    @staticmethod
    async def get_by_id(db: AsyncSession, pro_id: int):
        result = await db.execute(
            select(Product).where(Product.pro_id == pro_id)
        )
        return result.scalar_one_or_none()

    # 제조사 기준 상품 단건 조회
    @staticmethod
    async def get_by_id_and_factory(db: AsyncSession, pro_id: int, fac_id: int):
        result = await db.execute(
            select(Product).where(
                Product.pro_id == pro_id,
                Product.fac_id == fac_id,
            )
        )
        return result.scalar_one_or_none()

    # 상품 수정
    @staticmethod
    async def update(db: AsyncSession, product: Product, product_data: ProductUpdate):
        if product_data.pro_category is not None:
            product.pro_category = product_data.pro_category

        if product_data.pro_name is not None:
            product.pro_name = product_data.pro_name

        if product_data.pro_price is not None:
            product.pro_price = product_data.pro_price

        return product

    # 상품 삭제
    @staticmethod
    async def delete(db: AsyncSession, product: Product):
        await db.delete(product)