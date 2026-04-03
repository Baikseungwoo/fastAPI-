from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from app.core.setting import setting

async_engine=create_async_engine(setting.db_url, echo=False)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

sync_engine=create_engine(setting.sync_db_url, pool_pre_ping=True)

Base=declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session