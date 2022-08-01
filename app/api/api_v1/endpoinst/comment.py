from datetime import datetime
from typing import Any
import crud
import models
import schemas
from api import deps  # type: ignore
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status

router = APIRouter()


@router.put("/{comment_id}", response_model=schemas.CommentInDBBase)
async def update_comment(*, comment_id: int, new_comment: str = Form(...), current_user: models.Users = Depends(deps.get_current_active_user)) -> Any:
    comment = await crud.comment.get(id=comment_id)
    if not bool(comment):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no comment with this ID")
    elif comment.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to do that!")

    new_comment_data: schemas.CommentUpdate = schemas.CommentUpdate.parse_obj({
        "post_id": comment.post_id,
        "comment": new_comment,
        "user_id": current_user.id,
        "comment_id": comment_id,
        "updated_at": datetime.utcnow(),
        "is_edited": True,
    })

    comment_db = await crud.comment.update(db_obj=comment, obj_in=new_comment_data)

    return comment_db


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_comment(comment_id: int, current_user: models.Users = Depends(deps.get_current_active_user)) -> None:
    comment = await crud.comment.get(id=comment_id)
    if not bool(comment):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no comment with this ID")
    elif comment.user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to do that!",
        )

    await crud.comment.delete(id=comment.id)
