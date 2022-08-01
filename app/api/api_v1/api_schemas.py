from datetime import datetime
from typing import List, Optional

import pydantic
from schemas.post import PostInDBBase
from schemas.user import User


class UserOut(pydantic.BaseModel):
    user: User
    followers_count: int
    follows_count: int
    avatar_url: Optional[str]
    is_me_follow: Optional[bool]


class FollowersOut(pydantic.BaseModel):
    user: User
    avatar_url: Optional[str]


class FollowsOut(FollowersOut):
    pass


class UserPostImagesOut(pydantic.BaseModel):
    url: str
    order: int


class UserPostsOut(pydantic.BaseModel):
    post: PostInDBBase
    images: List[UserPostImagesOut]


class CommentsOut(pydantic.BaseModel):
    id: int
    poster: User
    poster_avatar_url: Optional[str]
    comment: str
    is_edited: bool
    created_at: datetime
    updated_at: datetime


class PostDataOut(pydantic.BaseModel):
    post: PostInDBBase
    images: List[UserPostImagesOut]
    likes_amount: int
    comments: List[CommentsOut]
    is_me_liked: Optional[bool]


class LikesOut(pydantic.BaseModel):
    user: User
    avatar_url: str
