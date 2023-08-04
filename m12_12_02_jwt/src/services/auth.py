from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer, JwtAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Security
from passlib.context import CryptContext
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "031f28c3ef1fd0e8f0fc7ab7733271b287226710988c431866dda957efa8ded6"

    # Read access token from bearer header and cookie (bearer priority)
    access_security = JwtAccessBearerCookie(
        secret_key=SECRET_KEY,
        auto_error=False,
        access_expires_delta=timedelta(hours=1)  # change access token validation timedelta
    )
    # Read refresh token from bearer header only
    refresh_security = JwtRefreshBearer(
        secret_key=SECRET_KEY,
        auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED
    )

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def get_jti(cls, token: str):
        token = jwt.decode(token, cls.SECRET_KEY, jwt.ALGORITHMS.HS256)
        return token.get("jti")


async def get_current_user(credentials: JwtAuthorizationCredentials = Security(Auth.access_security),
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    user = await repository_users.get_user_by_email(credentials["email"], db)
    if user is None:
        raise credentials_exception
    return user
