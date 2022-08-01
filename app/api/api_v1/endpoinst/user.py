# type: ignore
from typing import Any, List, Literal

import crud
import models
import schemas
from api import deps
from api.api_v1.api_schemas import (FollowersOut, FollowsOut, UserOut,
                                    UserPostsOut)
from core.settings import settings
from data.post_statuses import Statuses
from email_utils import send_new_account_email
from fastapi import (APIRouter, BackgroundTasks, Depends, HTTPException)

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def me(current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    avatar = await crud.avatar.get_by_user_id(user_id=current_user.id)
    followers_count = await crud.follower.get_user_followers_count(user_id=current_user.id)
    follows_count = await crud.follower.get_user_follows_count(user_id=current_user.id)
    return {"user": current_user, "followers_count": followers_count, "follows_count": follows_count, "avatar_url": avatar.url if avatar else None, "is_me_follow": None}


@router.post("", response_model=schemas.User, status_code=201)
async def create_user(*, user_in: schemas.UserCreate, background_task: BackgroundTasks) -> Any:
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.get_by_username(username=user_in.user_name)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        background_task.add_task(send_new_account_email, email_to=user_in.email,
                                 full_name=user_in.full_name, username=user_in.user_name, password=user_in.password)
    return user


@router.get("/{user_id}", response_model=UserOut)
async def read_user_by_id(
    user_id: int,
    current_user: models.Users = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(id=user_id)
    avatar = await crud.avatar.get_by_user_id(user_id=user_id)
    followers_count = await crud.follower.get_user_followers_count(user_id=user_id)
    follows_count = await crud.follower.get_user_follows_count(user_id=user_id)
    is_me_follow = await crud.follower.is_me_follow(user_id=user_id, me_id=current_user.id)
    return {"user": user, "followers_count": followers_count, "follows_count": follows_count, "avatar_url": avatar.url if avatar else None, "is_me_follow": is_me_follow}


@router.get("/{user_id}/posts/{status}", response_model=List[UserPostsOut])
async def get_user_posts(user_id: int, status: Literal["online", "archived"], current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    post_response = []

    if status.upper() == Statuses.ONLINE.value:
        posts = await crud.post.get_user_posts_online(user_id=user_id)
    elif status.upper() == Statuses.ARCHIVED.value:
        posts = await crud.post.get_user_posts_archived(user_id=user_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Please check correct post status (online, archived)!"
        )

    for post in posts:
        post_images_response = []
        postimages = await crud.postimage.get_by_post_id(post_id=post.id)

        for index, image in enumerate(postimages):
            postimage = await crud.image.get(id=image.id)
            post_images_response.append(
                {"url": postimage.url if postimage else None, "order": index})

        post_response.append({"post": post, "images": post_images_response})

    return post_response


@router.get("/{user_id}/followers", response_model=List[FollowersOut])
async def get_user_followers(user_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    followers_response = []
    followers = await crud.follower.get_user_followers(user_id=user_id)

    for follower in followers:
        follower_data = await crud.user.get(id=follower.follower_id)
        avatar = await crud.avatar.get_by_user_id(user_id=follower_data.id)
        followers_response.append(
            {"user": follower_data, "avatar_url": avatar.url if avatar else None})

    return followers_response


@router.get("/{user_id}/follows", response_model=List[FollowsOut])
async def get_user_follows(user_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    follows_response = []
    follows = await crud.follower.get_user_follows(user_id=user_id)

    for follow in follows:
        follow_data = await crud.user.get(id=follow.follow_id)
        avatar = await crud.avatar.get_by_user_id(user_id=follow_data.id)
        follows_response.append({
            "user": follow_data, "avatar_url": avatar.url if avatar else None
        })

    return follows_response
