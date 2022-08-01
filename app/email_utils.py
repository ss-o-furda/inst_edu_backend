import logging
from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

import crud
import schemas
from core.settings import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: int) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "token": token,
        },
    )


def send_new_account_email(email_to: str, full_name: Optional[str], username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "full_name": full_name or username,
            "user_name": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


async def generate_password_reset_token(email: str) -> int:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    random_digits = generate_6_random_digits()
    user = await crud.user.get_by_email(email=email)
    token_data: schemas.PasswordResetTokenCreate = schemas.PasswordResetTokenCreate.parse_obj({
        "token": random_digits,
        "user_id": user.id if user else None,
        "expire_at": expires
    })
    await crud.reset_token.create(obj_in=token_data)

    return random_digits


def generate_6_random_digits():
    range_start = 10**(5)
    range_end = (10**6)-1
    return randint(range_start, range_end)
