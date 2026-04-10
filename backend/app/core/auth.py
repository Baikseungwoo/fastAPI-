from typing import Optional

from fastapi import HTTPException, Request, Response
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.jwt_handle import (
    create_token,
    decode_token,
    get_pw_hash,
    verify_pw,
    verify_token,
)
from app.core.setting import setting


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(setting.access_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=int(setting.refresh_token_expire_seconds),
        secure=False,
        httponly=True,
        samesite="Lax",
    )


def create_access_token(data: dict) -> str:
    sub = data.get("sub")
    if sub is None:
        raise HTTPException(status_code=400, detail="token subject is required")

    uid = int(sub)
    extra_claims = {k: v for k, v in data.items() if k != "sub"}

    return create_token(
        uid=uid,
        expires_delta=setting.access_token_expire_seconds,
        sub=str(sub),
        **extra_claims,
    )


async def get_password_hash(password: str) -> str:
    return get_pw_hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return verify_pw(plain_password, hashed_password)


async def get_user_id(request: Request) -> int:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="access token not found")

    try:
        user_id = verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="invalid token payload")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid access token")


async def get_factory_id(request: Request) -> int:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="access token not found")

    try:
        payload = decode_token(access_token)
        uid = payload.get("uid")
        role = payload.get("role")

        if uid is None:
            raise HTTPException(status_code=401, detail="invalid token payload")
        if role != "factory":
            raise HTTPException(status_code=403, detail="factory account required")

        return int(uid)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid access token")


async def get_optional(request: Request) -> Optional[int]:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None

    try:
        return verify_token(access_token)
    except (ExpiredSignatureError, InvalidTokenError):
        return None
