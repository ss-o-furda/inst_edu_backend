# type: ignore
from datetime import datetime
from typing import Any, List

import crud
import models
import schemas
from api import deps
from api.api_v1.api_schemas import LikesOut, PostDataOut, UserPostsOut
from api.api_v1.utils.common import get_file_ext, write_new_file
from core.settings import settings
from fastapi import (APIRouter, Depends, File, Form, Response, UploadFile,
                     status)

router = APIRouter()


@router.get("/{post_id}", response_model=PostDataOut)
async def get_post_data(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    postimages_response = []
    postcomments_response = []
    post = await crud.post.get(id=post_id)

    postimages = await crud.postimage.get_by_post_id(post_id=post_id)

    for postimage in postimages:
        postimage_image = await crud.image.get(id=postimage.id)
        postimages_response.append(
            {"url": postimage_image.url if postimage_image else None, "order": postimage.order})

    post_comments = await crud.comment.get_by_post_id(post_id=post_id)

    for comment in post_comments:
        poster = await crud.user.get(id=comment.user_id)
        poster_avatar = await crud.avatar.get_by_user_id(user_id=poster.id)
        postcomments_response.append({
            "id": comment.id,
            "poster": poster,
            "poster_avatar_url": poster_avatar.url if poster_avatar else None,
            "comment": comment.comment,
            "created_at": comment.created_at,
            "is_edited": comment.is_edited,
            "updated_at": comment.updated_at,
        })

    post_likes_amount = await crud.like.get_post_likes_amount(post_id=post_id)

    is_me_liked = await crud.like.is_me_liked(post_id=post_id, me_id=current_user.id)

    return {"post": post, "images": postimages_response, "likes_amount": post_likes_amount, "comments": postcomments_response, "is_me_liked": is_me_liked}


@router.post("", response_model=UserPostsOut)
async def create_post(*, post_images: List[UploadFile] = File(...), description: str = Form(...), current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    post_images_response = []
    post_data: schemas.PostCreate = schemas.PostCreate.parse_obj(
        {"description": description, "poster_id": current_user.id})

    post = await crud.post.create(obj_in=post_data)

    for index, image in enumerate(post_images):
        location = f"{settings.POST_IMAGES_FOLDER}/{post.id}_{index}{get_file_ext(file=image)}"
        image_data: schemas.ImageCreate = schemas.ImageCreate.parse_obj({
            "image": location,
            "url": location,
        })

        await write_new_file(file_location=location, file=image)

        image_db = await crud.image.create(obj_in=image_data)

        postimage_data: schemas.PostImageCreate = schemas.PostImageCreate.parse_obj({
            "post_id": post.id,
            "image_id": image_db.id,
            "order": index,
        })

        postimage = await crud.postimage.create(obj_in=postimage_data)
        postimage_image = await crud.image.get(postimage.image_id)

        post_images_response.append(
            {"url": postimage_image.url if postimage_image else None, "order": postimage.order})

    return {"post": post, "images": post_images_response}


@router.put("/{post_id}", response_model=schemas.PostInDBBase)
async def edit_post(*, post_id: int, description: str = Form(...), current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    post = await crud.post.get(id=post_id)

    if not bool(post):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post with this ID")
    elif post.poster_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to do that!")

    new_post_data: schemas.PostUpdate = schemas.PostUpdate.parse_obj({
        "poster_id": current_user.id,
        "description": description,
        "is_edited": True,
        "updated_at": datetime.utcnow(),
    })

    new_post_db = await crud.post.update(db_obj=post, obj_in=new_post_data)

    return new_post_db


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def archive_post(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    post = await crud.post.get(id=post_id)
    if not bool(post):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post with this ID")
    elif post.poster_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to do that!")

    await crud.post.archive(id=post_id)


@router.patch("/{post_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def unarchive_post(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    post = await crud.post.get(id=post_id)
    if not bool(post):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no post with this ID")
    elif post.poster_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to do that!")

    await crud.post.unarchive(id=post_id)

# likes block


@router.get("/{post_id}/likes", response_model=List[LikesOut])
async def get_likes(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    likes_response = []
    likes = await crud.like.get_post_likes(post_id=post_id)
    for like in likes:
        user = await crud.user.get(id=like.user_id)
        avatar = await crud.avatar.get_by_user_id(user_id=user.id)
        likes_response.append(
            {"user": user, "avatar_url": avatar.url if avatar else None})

    return likes_response


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED, response_class=Response)
async def like_post(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> None:
    await crud.like.create(post_id=post_id, user_id=current_user.id)


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def dislike_post(post_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> None:
    await crud.like.delete_user_like(post_id=post_id, user_id=current_user.id)


# comments block

@router.post("/{post_id}/comment", response_model=schemas.CommentInDBBase)
async def create_comment(*, post_id: int, comment: str = Form(...), current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    comment_data: schemas.CommentCreate = schemas.CommentCreate.parse_obj({
        "post_id": post_id,
        "user_id": current_user.id,
        "comment": comment,
    })

    comment_db = await crud.comment.create(obj_in=comment_data)

    return comment_db
