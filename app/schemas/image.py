from datetime import datetime

from pydantic import BaseModel


class AvatarBase(BaseModel):
    user_id: int
    image: str
    url: str


class AvatarCreate(AvatarBase):
    pass


class AvatarUpdate(AvatarBase):
    pass


class AvatarInDBBase(AvatarBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    image: str
    url: str


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageInDBBase(ImageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
