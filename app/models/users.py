# type: ignore
from datetime import datetime
from typing import TYPE_CHECKING

from data.sexes import Sexes
from db.model_base import SqlAlchemyBase
from pydantic import EmailStr
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, Text)

if TYPE_CHECKING:
    from models.posts import Posts


class Users(SqlAlchemyBase):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    full_name: str = Column(String)
    user_name: str = Column(String, unique=True, index=True, nullable=False)
    email: EmailStr = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    sex: str = Column(Enum(Sexes, values_callable=lambda obj: [
                      e.value for e in obj]), default="NOT SPECIFIED", index=True)
    birth_date: datetime = Column(DateTime, index=True)
    web_site: str = Column(String)
    bio: str = Column(Text)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    last_login: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)


class Followers(SqlAlchemyBase):
    __tablename__ = "followers"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    follow_id: int = Column(Integer, ForeignKey('users.id'),
                            nullable=False)  # current active user
    # user who follow user with user_id
    follower_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)


class PasswordResetToken(SqlAlchemyBase):
    __tablename__ = "reset_password_code"

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    token: int = Column(Integer, unique=True, index=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    expire_at: datetime = Column(DateTime, index=True, nullable=False)
