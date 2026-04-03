from fastapi import FastAPI, Request
from app.core.jwt_handle import verify_token, create_access_token, create_refresh_token
from app.core.auth import set_auth_cookies
# from app.db.crud import UserCrud
# from app.db.database import get_db
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import ExpiredSignatureError, InvalidTokenError
