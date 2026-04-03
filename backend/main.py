import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from app.routers import user, board
from app.db.database import Base, async_engine
from app.middleware.token_refresh import RefreshTokenMiddleware
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# DB 연결 후 테이블 생성
# 종료 시 DB 연결 해제
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)

app.add_middleware(RefreshTokenMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(경로.router) 연결해야 함
