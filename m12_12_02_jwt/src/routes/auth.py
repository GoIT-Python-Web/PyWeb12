from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import UserSchema, UserResponseSchema, TokenModel
from src.repository import users as repository_users
from src.services.auth import Auth

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = Auth.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return new_user


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not Auth.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    subject = {"username": user.username, "email": user.email, "role": user.role.name}
    access_token = Auth.access_security.create_access_token(subject=subject)
    refresh_token = Auth.refresh_security.create_refresh_token(subject=subject)
    await repository_users.update_token(user, Auth.get_jti(refresh_token), db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: JwtAuthorizationCredentials = Security(Auth.refresh_security),
                        db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_email(credentials["email"], db)
    if user.refresh_token != credentials.jti:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    subject = {"username": user.username, "email": user.email, "role": user.role.name}
    access_token = Auth.access_security.create_access_token(subject=subject)
    refresh_token = Auth.refresh_security.create_refresh_token(subject=subject)
    await repository_users.update_token(user, Auth.get_jti(refresh_token), db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
