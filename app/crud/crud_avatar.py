from typing import Optional
from db.session import create_async_session
from models.images import Avatars
from schemas.image import AvatarCreate, AvatarUpdate
from sqlalchemy.future import select

from crud.base import CRUDBase


class CRUDAvatar(CRUDBase[Avatars, AvatarCreate, AvatarUpdate]):
    async def get_by_user_id(self, *, user_id: int) -> Optional[Avatars]:
        async with create_async_session() as session:
            query = select(Avatars).filter(Avatars.user_id == user_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def create(self, *, obj_in: AvatarCreate) -> Avatars:
        # remove old avatar from DB
        await self.remove_by_user_id(user_id=obj_in.user_id)

        db_obj = Avatars(
            user_id=obj_in.user_id,
            image=obj_in.image,
            url=obj_in.url
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def remove_by_user_id(self, user_id: int) -> None:
        async with create_async_session() as session:
            res = await self.get_by_user_id(user_id=user_id)
            if res:
                await session.delete(res)
                await session.commit()


avatar = CRUDAvatar(Avatars)
