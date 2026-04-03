from fastapi import FastAPI, Request
from app.core.jwt_handle import verify_token, create_access_token, create_refresh_token
from app.core.auth import set_auth_cookies
# from app.db.crud import UserCrud
from app.db.database import get_db
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError

class RefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        response=await call_next(request)

        # 쿠키에서 토큰 가져오기
        access_token=request.cookies.get('access_token')
        refresh_token=request.cookies.get('refresh_token')

        # 엑세스 토큰 존재 및 유효성 검증
        try:
            if access_token:
                verify_token(access_token)
                return response
        except (ExpiredSignatureError, InvalidTokenError):
            pass

        # 리프레시 토큰 존재 및 유효성 검증
        if refresh_token:
            try:
                user_id=verify_token(refresh_token)
            except (ExpiredSignatureError, InvalidTokenError):
                return response
            
            new_access_token=create_access_token(user_id)
            new_refresh_token=create_refresh_token(user_id)

            # DB에 새 리프레시 토큰 저장
            try:
                db=await anext(get_db())
                # await UserCrud.update_refresh_token_by_id(db, user_id, new_refresh_token)
                await db.commit()
            except Exception:
                await db.rollback()
                raise

            set_auth_cookies(response, new_access_token, new_refresh_token)

        return response