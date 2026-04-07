# app/routers/purchase.py
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_user_id
from app.db.database import get_db
from app.db.scheme.purchase import PurchaseCreate, PurchaseRead
from app.services.purchase import PurchaseService


router = APIRouter(prefix="/purchases", tags=["purchases"])


class ProductIdsRequest(BaseModel):
    product_ids: list[int]


@router.post("",response_model=PurchaseRead,status_code=status.HTTP_201_CREATED)
async def create_purchase(purchase_data: PurchaseCreate,db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await PurchaseService.create_purchase(db, user_id, purchase_data)


@router.post("/bulk",response_model=list[PurchaseRead],status_code=status.HTTP_201_CREATED)
async def create_purchases_bulk(payload: ProductIdsRequest,db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await PurchaseService.create_purchases_from_product_ids(
        db, user_id, payload.product_ids
    )


@router.get("",response_model=list[PurchaseRead],status_code=status.HTTP_200_OK)
async def get_my_purchases(db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await PurchaseService.get_my_purchases(db, user_id)


@router.get("/{purchase_id}",response_model=PurchaseRead,status_code=status.HTTP_200_OK)
async def get_my_purchase( purchase_id: int,db: AsyncSession = Depends(get_db),user_id: int = Depends(get_user_id)):
    return await PurchaseService.get_my_purchase(db, user_id, purchase_id)
