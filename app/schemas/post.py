from datetime import datetime
from typing import Optional

from data.post_statuses import Statuses
from pydantic import BaseModel


class PostBase(BaseModel):
    poster_id: int
    description: Optional[str] = None


class PostCreate(PostBase):
    status: Statuses = Statuses.ONLINE


class PostUpdate(PostBase):
    is_edited: bool = True
    updated_at: datetime


class PostInDBBase(PostBase):
    id: int
    status: Statuses
    is_edited: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    post_id: int
    user_id: int


class LikeCreate(LikeBase):
    pass


class LikeUpdate(LikeBase):
    pass


class LikeInDBBase(LikeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostImageBase(BaseModel):
    post_id: int
    image_id: int
    order: int


class PostImageCreate(PostImageBase):
    pass


class PostImageUpdate(PostImageBase):
    pass


class PostImageInDBBase(PostImageBase):
    id: int

    class Config:
        orm_mode = True
