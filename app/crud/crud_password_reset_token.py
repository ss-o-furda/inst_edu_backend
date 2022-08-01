from datetime import datetime
from sqlalchemy.future import select
from typing import List, Optional
from db.session import create_async_session
from crud.base import CRUDBase
from models.users import PasswordResetToken
from schemas.password_reset_token import PasswordResetTokenCreate, PasswordResetTokenUpdate


class CRUDResetToken(CRUDBase[PasswordResetToken, PasswordResetTokenCreate, PasswordResetTokenUpdate]):
    async def get_by_code(self, code: int) -> Optional[PasswordResetToken]:
        async with create_async_session() as session:
            query = select(PasswordResetToken).filter(PasswordResetToken.token == code)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def create(self, *, obj_in: PasswordResetTokenCreate) -> PasswordResetToken:
        db_obj = PasswordResetToken(
            token=obj_in.token,
            user_id=obj_in.user_id,
            expire_at=obj_in.expire_at
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def delete(self, id: int) -> None:
        async with create_async_session() as session:
            get_query = select(PasswordResetToken).filter(PasswordResetToken.id == id)
            result = await session.execute(get_query)
            scalar = result.scalar()
            if scalar:
                await session.delete(scalar)
                await session.commit()

reset_token = CRUDResetToken(PasswordResetToken)
