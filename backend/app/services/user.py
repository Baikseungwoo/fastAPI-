from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.models import User
from app.db.crud import UserCrud
from app.db.scheme.user import CreateUser, LoginUser
from app.core.jwt_handle import (
    get_pw_hash, verify_pw, create_access_token, create_refresh_token
)

class UserService:

    # 회원가입
    @staticmethod
    async def signup(db:AsyncSession, user:CreateUser):
        if await UserCrud.get_by_name(db, user.use_name):
            raise HTTPException(status_code=400, detail='이미 사용중인 이름입니다.')
        
        hash_pw=get_pw_hash(user.password)
        user_create=CreateUser(username=user.use_name, password=hash_pw, email=user.use_email)

        try:
            db_user=await UserCrud.create(db, user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=401, detail='잘못된 이메일 또는 비밀번호입니다.')

    # 로그인
    @staticmethod
    async def login(db:AsyncSession, user:LoginUser):
        db_user=await UserCrud.get_by_email(db, user.use_email)
        if not db_user or not verify_pw(user.password, db_user.use_password):
            raise HTTPException(status_code=401, detail='잘못된 이메일 또는 비밀번호입니다.')

        refresh_token=create_refresh_token(db_user.use_id)
        access_token=create_access_token(db_user.use_id)

        await UserCrud.update_refresh_token_by_id(db, db_user.use_id, refresh_token)
        await db.commit()

        return db_user, access_token, refresh_token

    # 사용자 정보
    @staticmethod
    async def get_user(db:AsyncSession, user_id:int)-> User:
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail='사용자를 찾을 수 없습니다.')
        return db_user
    
    # 이메일 재설정
    @staticmethod
    async def update_email(db:AsyncSession, user_id:int, old_email:str, new_email:str):
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail='사용자를 찾을 수 없습니다.')
        
        if await UserCrud.get_by_email(db, new_email):
            raise HTTPException(status_code=400, detail='이미 사용중인 이메일입니다.')
        
        try:
            updated_user=await UserCrud.update_email_by_id(db, user_id, new_email)
            await db.commit()
            await db.refresh(updated_user)
            return updated_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail='이메일 수정 중 오류가 발생했습니다.')

    # 비밀번호 재설정 
    @staticmethod
    async def update_password(db:AsyncSession, user_id:int, old_password:str, new_password:str):
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail='사용자를 찾을 수 없습니다.')
        
        # 기존 비밀번호 검증 (use_password)
        if not verify_pw(old_password, db_user.use_password):
            raise HTTPException(status_code=401, detail='비밀번호가 일치하지 않습니다.')

        # 새 비밀번호 해싱
        hashed_pw=get_pw_hash(new_password)
        
        try:
            updated_user=await UserCrud.update_pw_by_id(db, user_id, hashed_pw)
            await db.commit()
            await db.refresh(updated_user)
            return updated_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail='비밀번호 수정 중 오류가 발생했습니다.')

    # 계정 삭제
    @staticmethod
    async def delete_user(db:AsyncSession, user_id:int, password:str):
        db_user=await UserCrud.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail='사용자를 찾을 수 없습니다.')
        
        # 비밀번호 최종 확인 (use_password)
        if not verify_pw(password, db_user.use_password):
            raise HTTPException(status_code=401, detail='비밀번호가 일치하지 않습니다.')

        try:
            await UserCrud.delete_by_id(db, user_id)
            await db.commit()
            return ('계정이 삭제되었습니다. 안녕히 가세요.')
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail='탈퇴 처리 중 오류가 발생했습니다.')