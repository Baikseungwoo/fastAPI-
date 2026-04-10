from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_factory_id
from app.db.database import get_db
from app.db.scheme.factory import FactoryCreate, FactoryLogin, UpdateFactory, FactoryRead, FactoryToken
from app.services.factory import FactoryService

router = APIRouter(prefix="/factory", tags=["factory"])


# 제조사 회원가입
@router.post("/signup", response_model=FactoryRead, status_code=status.HTTP_201_CREATED)
async def signup_factory(factory_data: FactoryCreate, db: AsyncSession = Depends(get_db)):
    return await FactoryService.create_factory(db, factory_data)


# 제조사 로그인
@router.post("/login", response_model=FactoryToken, status_code=status.HTTP_200_OK)
async def login_factory(factory_data: FactoryLogin, db: AsyncSession = Depends(get_db)):
    return await FactoryService.login_factory(db, factory_data)


# 내 정보 조회
@router.get("/me", response_model=FactoryRead, status_code=status.HTTP_200_OK)
async def get_my_factory(db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await FactoryService.get_my_factory(db, fac_id)


# 내 정보 수정
@router.put("/me", response_model=FactoryRead, status_code=status.HTTP_200_OK)
async def update_my_factory(factory_data: UpdateFactory, db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await FactoryService.update_factory(db, fac_id, factory_data)


# 계정 삭제
@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_my_factory(db: AsyncSession = Depends(get_db), fac_id: int = Depends(get_factory_id)):
    return await FactoryService.delete_factory(db, fac_id)
