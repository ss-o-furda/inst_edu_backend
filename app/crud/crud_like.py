from typing import List
from db.session import create_async_session
from models.posts import Likes
from schemas.post import LikeCreate, LikeUpdate
from sqlalchemy.future import select
from sqlalchemy import func, desc

from crud.base import CRUDBase


class CRUDLike(CRUDBase[Likes, LikeCreate, LikeUpdate]):
    async def get_post_likes_amount(self, post_id: int) -> int:
        async with create_async_session() as session:
            query = select(func.count()).filter(Likes.post_id == post_id)
            result = await session.execute(query)

            return result.scalar()

    async def get_post_likes(self, post_id: int) -> List[Likes]:
        async with create_async_session() as session:
            query = select(Likes).filter(Likes.post_id ==
                                         post_id).order_by(desc(Likes.created_at))
            result = await session.execute(query)

            return result.scalars().all()

    async def create(self, *, post_id: int, user_id: int) -> Likes:
        db_obj = Likes(
            user_id=user_id,
            post_id=post_id
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def delete_user_like(self, post_id: int, user_id: int) -> None:
        async with create_async_session() as session:
            query = select(Likes).filter(Likes.post_id ==
                                         post_id).filter(Likes.user_id == user_id)
            result = await session.execute(query)

            await session.delete(result.scalar())
            await session.commit()

    async def is_me_liked(self, post_id: int, me_id: int) -> bool:
        async with create_async_session() as session:
            query = select(Likes).filter(Likes.post_id ==
                                         post_id).filter(Likes.user_id == me_id)
            result = await session.execute(query)

            return bool(result.scalar_one_or_none())


like = CRUDLike(Likes)
