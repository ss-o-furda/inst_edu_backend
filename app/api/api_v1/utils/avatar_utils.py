import os

import aiofiles
import schemas
from core.settings import settings
from .common import get_file_ext
from fastapi import UploadFile


def remove_old_avatar_from_folder(user_id: int) -> None:
    for file in os.listdir(settings.AVATARS_FOLDER):
        if file.startswith(f'{user_id}.'):
            os.remove(f"{settings.AVATARS_FOLDER}/{file}")


def get_avatar_location(user_id: int, avatar: UploadFile) -> str:
    return f"{settings.AVATARS_FOLDER}/{user_id}{get_file_ext(file=avatar)}"


def parse_schema_object(obj_in: dict) -> schemas.AvatarCreate:
    return schemas.AvatarCreate.parse_obj(obj_in)
