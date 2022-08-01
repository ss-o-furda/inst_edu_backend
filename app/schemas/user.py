from datetime import datetime
from typing import Any, Optional
from schemas.image import AvatarInDBBase

from data.sexes import Sexes
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: Optional[str] = None
    user_name: str
    email: EmailStr
    sex: Sexes
    birth_date: datetime
    web_site: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    updated_at: datetime


class UserChangeLastLogin(BaseModel):
    last_login: datetime


class UserChangePassword(BaseModel):
    new_password: str


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
