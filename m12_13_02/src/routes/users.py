from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import config
from src.schemas import UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])

cloudinary.config(
    cloud_name=config.cloudinary_name,
    api_key=config.cloudinary_api_key,
    api_secret=config.cloudinary_api_secret,
    secure=True
)


@router.get("/me/", response_model=UserResponseSchema)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserResponseSchema)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):

    r = cloudinary.uploader.upload(file.file, public_id=f'TODOApp/{current_user.username}', overwrite=True)

    src_url = cloudinary.CloudinaryImage(f'TODOApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
