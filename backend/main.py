from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from app.db.database import Base, async_engine
from app.middleware.token_refresh import RefreshTokenMiddleware
from app.routers import user

@asynccontextmanager
async def lifespan(app:FastAPI):
    # 앱 시작 시 테이블 생성
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 앱 종료 시 리소스 정리
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)


# app.include_router(경로.router) 연결
app.include_router(user.router)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RefreshTokenMiddleware)