from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_factory_id
from app.db.database import get_db
from app.db.scheme.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/product", tags=["product"])


@router.post("/items", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await ProductService.create_product(db, fac_id, product_data)


@router.get("/items", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get_my_products(
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await ProductService.get_my_products(db, fac_id)


@router.get("/items/{pro_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def get_my_product(
    pro_id: int,
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await ProductService.get_my_product(db, fac_id, pro_id)


@router.put("/items/{pro_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update_product(
    pro_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await ProductService.update_product(db, fac_id, pro_id, product_data)


@router.delete("/items/{pro_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    pro_id: int,
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await ProductService.delete_product(db, fac_id, pro_id)