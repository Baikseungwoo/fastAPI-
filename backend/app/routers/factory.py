from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_factory_id
from app.db.database import get_db
from app.db.scheme.factory import FactoryCreate, FactoryRead, FactoryUpdate
from app.db.scheme.auth import LoginRequest, Token
from app.services.factory import FactoryService

router = APIRouter(prefix="/factory", tags=["factory"])


@router.post("/register", response_model=FactoryRead, status_code=status.HTTP_201_CREATED)
async def create_factory(
    factory_data: FactoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await FactoryService.create_factory(db, factory_data)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_factory(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await FactoryService.login_factory(db, login_data)


@router.get("/me", response_model=FactoryRead, status_code=status.HTTP_200_OK)
async def get_my_factory(
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await FactoryService.get_my_factory(db, fac_id)


@router.put("/me", response_model=FactoryRead, status_code=status.HTTP_200_OK)
async def update_my_factory(
    factory_data: FactoryUpdate,
    db: AsyncSession = Depends(get_db),
    fac_id: int = Depends(get_factory_id)
):
    return await FactoryService.update_my_factory(db, fac_id, factory_data)