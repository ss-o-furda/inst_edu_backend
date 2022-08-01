from datetime import datetime, timedelta
from typing import Any
from email_utils import generate_password_reset_token, send_reset_password_email

import crud
import schemas
from core import security
from core.settings import settings
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}")
async def recover_password(email: str, background_task: BackgroundTasks) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = await generate_password_reset_token(email=email)
    if settings.EMAILS_ENABLED and user and user.email:
        background_task.add_task(send_reset_password_email, email_to=user.email,
                                 email=email, token=password_reset_token)

    return {"msg": "Password recovery email sent"}


@router.post("/reset-password")
async def reset_password(token: int = Form(...), new_password: str = Form(...)) -> Any:
    token = await crud.reset_token.get_by_code(code=token)
    if not token:
        raise HTTPException(
            status_code=404,
            detail="Cannot find your reset token!",
        )
    if datetime.utcnow() > token.expire_at:
        raise HTTPException(
            status_code=400,
            detail="Your token expired!",
        )
    user = await crud.user.get(id=token.user_id)

    new_password_obj: schemas.UserChangePassword = schemas.UserChangePassword.parse_obj({
        "new_password": new_password
    })

    await crud.user.change_password(db_obj=user, obj_in=new_password_obj)

    await crud.reset_token.delete(id=token.id)

    return {"msg": "Password updated successfully"}
