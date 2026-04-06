from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.purchase import PurchaseCrud
from app.db.scheme.purchase import PurchaseCreate


class PurchaseService:
    @staticmethod
    async def create_purchase(
        db: AsyncSession,
        user_id: int,
        purchase_data: PurchaseCreate,
    ):
        try:
            purchase = await PurchaseCrud.create(db, user_id, purchase_data)
            await db.commit()
            await db.refresh(purchase)
            return purchase
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def create_purchases_from_product_ids(
        db: AsyncSession,
        user_id: int,
        product_ids: list[int],
    ):
        if not product_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="구매할 상품이 없습니다.",
            )

        try:
            purchases = await PurchaseCrud.create_many_by_product_ids(
                db, user_id, product_ids
            )
            await db.commit()
            for purchase in purchases:
                await db.refresh(purchase)
            return purchases
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_my_purchases(db: AsyncSession, user_id: int):
        return await PurchaseCrud.get_list_by_user(db, user_id)

    @staticmethod
    async def get_my_purchase(db: AsyncSession, user_id: int, purchase_id: int):
        purchase = await PurchaseCrud.get_by_id_and_user(db, purchase_id, user_id)
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="구매 내역을 찾을 수 없습니다.",
            )
        return purchase
