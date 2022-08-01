from datetime import datetime
from typing import Any
import crud
import models
import schemas
from api import deps  # type: ignore
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status

router = APIRouter()


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED, response_class=Response)
async def follow_user(user_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    is_already_follow = await crud.follower.is_me_follow(user_id=user_id, me_id=current_user.id)
    if is_already_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already follow this user!")

    follow_create_data: schemas.FollowerCreate = schemas.FollowerCreate.parse_obj({
        "follow_id": current_user.id,
        "follower_id": user_id,
    })
    await crud.follower.create(obj_in=follow_create_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def unfollow_user(user_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    is_already_follow = await crud.follower.is_me_follow(user_id=user_id, me_id=current_user.id)
    if not is_already_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You not follow this user!")

    follow_db = await crud.follower.get_current_follow(user_id=user_id, me_id=current_user.id)
    if follow_db:
        await crud.follower.delete(id=follow_db.id)
