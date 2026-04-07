from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_user_id
from app.db.database import get_db
from app.db.scheme.cart import CartCreate, CartRead
from app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/items",response_model=CartRead,status_code=status.HTTP_201_CREATED)
async def add_cart_item(cart_data: CartCreate,db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await CartService.add_to_cart(db, user_id, cart_data)


@router.get("/items",response_model=list[CartRead],status_code=status.HTTP_200_OK)
async def get_my_cart(db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await CartService.get_my_cart(db, user_id)


@router.get("/items/{cart_id}",response_model=CartRead,status_code=status.HTTP_200_OK)
async def get_my_cart_item(cart_id: int,db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await CartService.get_my_cart_item(db, user_id, cart_id)


@router.delete("/items/{cart_id}",status_code=status.HTTP_200_OK,)
async def delete_cart_item(cart_id: int, db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await CartService.remove_cart_item(db, user_id, cart_id)


@router.delete("/items",status_code=status.HTTP_200_OK)
async def clear_my_cart( db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await CartService.clear_my_cart(db, user_id)
