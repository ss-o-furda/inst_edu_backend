# type: ignore
from datetime import datetime
from typing import TYPE_CHECKING

from data.post_statuses import Statuses
from db.model_base import SqlAlchemyBase
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        Text)
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.users import Users


class Posts(SqlAlchemyBase):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    poster_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    description: str = Column(Text)
    status: str = Column(Enum(Statuses, values_callable=lambda obj: [
        e.value for e in obj]), index=True)
    is_edited: bool = Column(Boolean(), default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)

    poster = relationship("Users", backref="posts")


class Likes(SqlAlchemyBase):
    __tablename__ = "likes"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    post_id: int = Column(ForeignKey("posts.id"), nullable=False)
    user_id: int = Column(ForeignKey("users.id"), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)

    post = relationship(Posts, backref="likes", order_by="-Likes.created_at")
    poster = relationship("Users", backref="likes")


class PostImages(SqlAlchemyBase):
    __tablename__ = "postimages"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    post_id: int = Column(Integer, ForeignKey('posts.id'), nullable=False)
    image_id: int = Column(Integer, ForeignKey('images.id'), nullable=False)
    order: int = Column(Integer, nullable=False)
