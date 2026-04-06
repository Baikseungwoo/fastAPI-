from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import Cart
from app.db.scheme.cart import CartCreate

class CartCrud:

    @staticmethod
    async def create(db:AsyncSession, user_id:int,  cart_data:CartCreate) -> Cart:
        cart_dict=cart_data.model_dump()
        cart_dict["use_id"]=user_id
        new_cart=Cart(**cart_dict)
        db.add(new_cart)
        await db.flush()
        return new_cart
    
    @staticmethod
    async def get_list_by_user(db: AsyncSession, user_id: int) -> list[Cart]:
        query = (
            select(Cart)
            .where(Cart.use_id == user_id)
            .order_by(Cart.created_at.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id_and_user(db: AsyncSession, cart_id: int, user_id: int) -> Cart | None:
        query = select(Cart).where(Cart.car_id == cart_id, Cart.use_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_user_and_product(db: AsyncSession, user_id: int, product_id: int) -> Cart | None:
        query = select(Cart).where(Cart.use_id == user_id, Cart.pro_id == product_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_one(db: AsyncSession, cart_id: int, user_id: int) -> bool:
        query = delete(Cart).where(Cart.car_id == cart_id, Cart.use_id == user_id)
        result = await db.execute(query)
        return (result.rowcount or 0) > 0

    @staticmethod
    async def clear(db: AsyncSession, user_id: int) -> int:
        query = delete(Cart).where(Cart.use_id == user_id)
        result = await db.execute(query)
        return result.rowcount or 0