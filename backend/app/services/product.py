from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.product import ProductCrud
from app.db.scheme.product import ProductCreate, ProductUpdate


class ProductService:

    # 상품 등록
    @staticmethod
    async def create_product(db: AsyncSession, fac_id: int, product_data: ProductCreate):
        try:
            product = await ProductCrud.create(db, fac_id, product_data)
            await db.commit()
            await db.refresh(product)
            return product
        except Exception:
            await db.rollback()
            raise

    # 상품 전체 조회
    @staticmethod
    async def get_product_list(db: AsyncSession):
        return await ProductCrud.get_list(db)

    # 상품 단건 조회
    @staticmethod
    async def get_product_detail(db: AsyncSession, pro_id: int):
        product = await ProductCrud.get_by_id(db, pro_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상품을 찾을 수 없습니다.",
            )
        return product

    # 내 상품 단건 조회
    @staticmethod
    async def get_my_product(db: AsyncSession, fac_id: int, pro_id: int):
        product = await ProductCrud.get_by_id_and_factory(db, pro_id, fac_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="상품을 찾을 수 없습니다.",
            )
        return product

    # 내 상품 수정
    @staticmethod
    async def update_product(
        db: AsyncSession,
        fac_id: int,
        pro_id: int,
        product_data: ProductUpdate,
    ):
        product = await ProductCrud.get_by_id_and_factory(db, pro_id, fac_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="수정할 상품을 찾을 수 없습니다.",
            )

        try:
            updated = await ProductCrud.update(db, product, product_data)
            await db.commit()
            await db.refresh(updated)
            return updated
        except Exception:
            await db.rollback()
            raise

    # 내 상품 삭제
    @staticmethod
    async def delete_product(db: AsyncSession, fac_id: int, pro_id: int):
        product = await ProductCrud.get_by_id_and_factory(db, pro_id, fac_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="삭제할 상품을 찾을 수 없습니다.",
            )

        try:
            await ProductCrud.delete(db, product)
            await db.commit()
            return {"message": "상품이 삭제되었습니다."}
        except Exception:
            await db.rollback()
            raise
