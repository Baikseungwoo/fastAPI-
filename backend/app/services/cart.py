# app/service/cart.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.cart import CartCrud
from app.db.scheme.cart import CartCreate


class CartService:
    @staticmethod
    async def add_to_cart(db: AsyncSession, user_id: int, cart_data: CartCreate):
        # 같은 상품 중복 담기 방지
        exists = await CartCrud.get_by_user_and_product(db, user_id, cart_data.pro_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 장바구니에 담긴 상품입니다.",
            )

        try:
            cart = await CartCrud.create(db, user_id, cart_data)
            await db.commit()
            await db.refresh(cart)
            return cart
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_my_cart(db: AsyncSession, user_id: int):
        return await CartCrud.get_list_by_user(db, user_id)

    @staticmethod
    async def get_my_cart_item(db: AsyncSession, user_id: int, cart_id: int):
        cart = await CartCrud.get_by_id_and_user(db, cart_id, user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="장바구니 항목을 찾을 수 없습니다.",
            )
        return cart

    @staticmethod
    async def remove_cart_item(db: AsyncSession, user_id: int, cart_id: int):
        cart = await CartCrud.get_by_id_and_user(db, cart_id, user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="장바구니 항목을 찾을 수 없습니다.",
            )

        try:
            ok = await CartCrud.delete_one(db, cart_id, user_id)
            await db.commit()
            return {"deleted": ok}
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def clear_my_cart(db: AsyncSession, user_id: int):
        try:
            deleted_count = await CartCrud.clear(db, user_id)
            await db.commit()
            return {"deleted_count": deleted_count}
        except Exception:
            await db.rollback()
            raise


