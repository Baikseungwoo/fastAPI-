from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Purchase
from app.db.scheme.purchase import PurchaseCreate


class PurchaseCrud:
    @staticmethod
    async def create(db: AsyncSession,user_id: int,purchase_data: PurchaseCreate) -> Purchase:
        payload = purchase_data.model_dump()
        payload["use_id"] = user_id

        new_purchase = Purchase(**payload)
        db.add(new_purchase)
        await db.flush()
        return new_purchase

    @staticmethod
    async def create_many_by_product_ids(db: AsyncSession,user_id: int,product_ids: list[int]) -> list[Purchase]:
        purchases = [Purchase(use_id=user_id, pro_id=pro_id) for pro_id in product_ids]
        db.add_all(purchases)
        await db.flush()
        return purchases

    @staticmethod
    async def get_list_by_user(db: AsyncSession, user_id: int) -> list[Purchase]:
        query = (
            select(Purchase)
            .where(Purchase.use_id == user_id)
            .order_by(Purchase.pur_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id_and_user(db: AsyncSession,purchase_id: int,user_id: int) -> Purchase | None:
        query = select(Purchase).where(
            Purchase.pur_id == purchase_id,
            Purchase.use_id == user_id,
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()