# type: ignore
from datetime import datetime
from typing import TYPE_CHECKING

from db.model_base import SqlAlchemyBase
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.users import Users


class Avatars(SqlAlchemyBase):
    __tablename__ = "avatars"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image: str = Column(String, index=True, unique=True, nullable=False)
    url: str = Column(String, unique=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("Users", backref="avatar", uselist=False)


class Images(SqlAlchemyBase):
    __tablename__ = "images"

    id: int = Column(Integer, primary_key=True,
                     autoincrement=True, index=True)
    image: str = Column(String, index=True, unique=True, nullable=False)
    url: str = Column(String, unique=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, index=True)
