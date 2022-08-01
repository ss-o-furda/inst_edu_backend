from typing import Any

import crud
import models
import schemas
from api import deps  # type: ignore
from api.api_v1.utils.avatar_utils import (get_avatar_location,
                                           parse_schema_object,
                                           remove_old_avatar_from_folder)
from api.api_v1.utils.common import write_new_file
from fastapi import APIRouter, Depends, File, UploadFile, status

router = APIRouter()


@router.post("", response_model=schemas.AvatarInDBBase, status_code=status.HTTP_201_CREATED)
async def create_avatar(avatar: UploadFile = File(...), current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:

    remove_old_avatar_from_folder(user_id=current_user.id)

    file_location = get_avatar_location(user_id=current_user.id, avatar=avatar)

    await write_new_file(file_location=file_location, file=avatar)

    avatar_info: schemas.AvatarCreate = parse_schema_object({
        "user_id": current_user.id,
        "image": file_location,
        "url": file_location
    })

    new_avatar = await crud.avatar.create(
        obj_in=avatar_info
    )
    return new_avatar
