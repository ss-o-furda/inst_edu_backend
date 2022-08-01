from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str
    post_id: int
    user_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    is_edited: bool = True
    updated_at: datetime


class CommentInDBBase(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReplyBase(BaseModel):
    comment_id: int


class ReplyCreate(ReplyBase):
    pass


class ReplyUpdate(ReplyBase):
    pass


class ReplyInDBBase(ReplyBase):
    id: int
    reply_id: int

    class Config:
        orm_mode = True
