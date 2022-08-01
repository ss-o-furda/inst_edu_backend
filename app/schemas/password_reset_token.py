from datetime import datetime
import pydantic


class PasswordResetTokenCreate(pydantic.BaseModel):
    token: int
    user_id: int
    expire_at: datetime


class PasswordResetTokenUpdate(PasswordResetTokenCreate):
    pass
