from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from backend.app.core.setting import settings
import uuid
import jwt

# 입력된 비밀번호 암호화
pw_crypt=CryptContext(schemes=['bcrypt'])

# 해싱
def get_pw_hash(pw:str):
    trunc_pw=pw.encode('utf-8')[:72]
    return pw_crypt.hash(trunc_pw)

# 입력값vs해시값 비교
def verify_pw(plain_pw:str, hashed_pw:str)->bool:
    trunc_pw=plain_pw.encode('utf-8')[:72]
    return pw_crypt.verify(trunc_pw, hashed_pw)

# 토큰 생성
def create_token(uid:int, expires_delta:timedelta, **kwargs)->str:
    to_encode=kwargs.copy()
    expire=datetime.now(timezone.utc)+timedelta(seconds=expires_delta)
    to_encode.update({'exp':expire, 'uid':uid})
    encoded_jwt=jwt.encode(to_encode, settings.secret_key, settings.jwt_algorithm)
    return encoded_jwt

# create_token 함수 호출-> jwt 생성
def create_access_token(uid:int)->str:
    return create_token(uid=uid, expires_delta=settings.access_token_expire_seconds)

# 리프레시 토큰 관리
def create_refresh_token(uid:int):
    return create_token(uid=uid, jti=str(uuid.uuid4()), expires_delta=settings.refresh_token_expire_seconds)

# 토큰 디코딩-> payload 딕셔너리로 반환 (검증: 변조 여부 확인)
def decode_token(token:str)->dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.jwt_algorithm]
    )

# 토큰 디코딩-> uid값 불러오기
def verify_token(token:str)->int:
    payload=decode_token(token)
    return payload.get('uid')