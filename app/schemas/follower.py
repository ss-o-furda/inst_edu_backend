from datetime import datetime

from pydantic import BaseModel


class FollowerBase(BaseModel):
    follow_id: int
    follower_id: int


class FollowerCreate(FollowerBase):
    pass

class FollowerUpdate(FollowerBase):
    pass

class FollowerInDBBase(FollowerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
