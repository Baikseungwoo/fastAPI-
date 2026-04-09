from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_factory_id
from app.db.database import get_db
from app.db.scheme.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/product", tags=["product"])


# 상품 등록
@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await ProductService.create_product(db, fac_id, product_data)


# 전체 상품 조회
@router.get("", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get_product_list(db: AsyncSession = Depends(get_db)):
    return await ProductService.get_product_list(db)


# 내 상품 조회
@router.get("/my", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get_my_product_list(db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await ProductService.get_my_product_list(db, fac_id)


# 상품 상세 조회
@router.get("/{pro_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def get_product(pro_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductService.get_product_by_id(db, pro_id)


# 상품 수정
@router.put("/{pro_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def update_product(pro_id: int, product_data: ProductUpdate, db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await ProductService.update_product(db, pro_id, fac_id, product_data)


# 상품 삭제
@router.delete("/{pro_id}", status_code=status.HTTP_200_OK)
async def delete_product(pro_id: int, db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await ProductService.delete_product(db, pro_id, fac_id)
