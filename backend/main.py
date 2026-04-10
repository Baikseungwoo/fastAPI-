from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import asynccontextmanager
from app.db.database import Base, async_engine
from app.middleware.token_refresh import RefreshTokenMiddleware
from app.routers.cart import router as cart_router
from app.routers.purchase import router as purchase_router
from app.routers.user import router as user_router
from app.routers.product import router as product_router
from app.routers.factory import router as factory_router


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
app.include_router(cart_router)
app.include_router(purchase_router)
app.include_router(user_router)
app.include_router(factory_router)
app.include_router(product_router)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RefreshTokenMiddleware)
