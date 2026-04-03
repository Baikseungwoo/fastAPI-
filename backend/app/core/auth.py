from fastapi import Request, Response, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from backend.app.core.setting import settings
from app.core.jwt_handle import verify_token
from typing import Optional

def set_auth_cookies(response:Response, access_token:str, refresh_token:str)->None:
    
    response.set_cookie(
        key='access_token',
        value=access_token,
        max_age=int(settings.access_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite='Lax',
    )
    
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        max_age=int(settings.refresh_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite='Lax',
    )

async def get_user_id(request:Request)->int:
    access_token=request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail='액세스 토큰을 찾을 수 없습니다')
    
    try:
        user_id=verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401, detail='no uid')
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='액세스 토큰이 만료되었습니다')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='유효하지 않은 액세스 토큰입니다')

async def get_optional(request:Request)-> Optional[int]:
    access_token=request.cookies.get('access_token')
    if not access_token:
        return None
    try:
        return verify_token(access_token)
    except (ExpiredSignatureError, InvalidTokenError):
        return None