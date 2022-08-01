# type: ignore
from datetime import datetime
from typing import TYPE_CHECKING

from db.model_base import SqlAlchemyBase
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.posts import Posts


class Comments(SqlAlchemyBase):
    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    comment: str = Column(Text, nullable=False)
    post_id: int = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_edited: bool = Column(Boolean(), default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)

    post = relationship("Posts", backref="comments", uselist=False)
    poster = relationship("Users", backref="comments", uselist=False)


class Replies(SqlAlchemyBase):
    __tablename__ = "replies"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    comment_id: int = Column(Integer, ForeignKey("comments.id"), nullable=False)
    reply_id: int = Column(Integer, ForeignKey("comments.id"), nullable=False)
