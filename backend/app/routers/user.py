from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.scheme.user import CreateUser, ReadUser, LoginUser, UpdateEmail, UpdatePassword, DeleteUser
from app.db.database import get_db
from app.services.user import UserService
from app.core.auth import set_auth_cookies, get_user_id

# 엔드 포인트
router=APIRouter(prefix='/user', tags=['User'])

# 회원가입
@router.post('/signup', response_model=ReadUser)
async def signup(user:CreateUser, db:AsyncSession=Depends(get_db)):
    db_user=await UserService.signup(db, user)
    return db_user

# 로그인
@router.post('/login', response_model=ReadUser)
async def login(user:LoginUser, response:Response, db:AsyncSession=Depends(get_db)):
    result=await UserService.login(db, user)
    db_user, acceess_token, refresh_token = result
    set_auth_cookies(response, acceess_token, refresh_token)
    return db_user

# 로그아웃
@router.post('/logout')
async def logout(response:Response):
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')
    return True

# 내 정보
@router.get('/me', response_model=ReadUser)
async def me(user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await UserService.get_user(db, user_id)

# 이메일 재설정
@router.post('/me/{use_email}', response_model=ReadUser)
async def update_email(email:UpdateEmail, user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    updated_email=await UserService.update_email(db, user_id, email.new_email)
    return updated_email

# 비밀번호 재설정 
@router.post('/password', response_model=ReadUser)
async def update_pw(pw:UpdatePassword, user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    updated_pw=await UserService.update_password(db, user_id, pw.old_password, pw.new_password)
    return updated_pw

# 탈퇴 (계정 삭제)
@router.delete('/me', status_code=200)
async def delete_acc(delete_data:DeleteUser, response:Response,
                     user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    result=await UserService.delete_user(db, user_id, delete_data.password)

    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return result