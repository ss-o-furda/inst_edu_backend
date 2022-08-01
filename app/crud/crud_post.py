from datetime import datetime
from sqlalchemy.future import select
from typing import List, Optional

from data.post_statuses import Statuses
from db.session import create_async_session
from models.posts import Posts
from schemas.post import PostCreate, PostUpdate

from crud.base import CRUDBase


class CRUDPost(CRUDBase[Posts, PostCreate, PostUpdate]):
    async def get_user_posts_online(self, *, user_id: int) -> List[Posts]:
        async with create_async_session() as session:
            query = select(Posts).filter(Posts.poster_id == user_id).filter(
                Posts.status == Statuses.ONLINE)
            result = await session.execute(query)

            return result.scalars().all()

    async def get_user_posts_archived(self, *, user_id: int) -> List[Posts]:
        async with create_async_session() as session:
            query = select(Posts).filter(Posts.poster_id == user_id).filter(
                Posts.status == Statuses.ARCHIVED)
            result = await session.execute(query)

            return result.scalars().all()

    async def create(self, *, obj_in: PostCreate) -> Posts:
        db_obj = Posts(
            poster_id=obj_in.poster_id,
            description=obj_in.description,
            status=Statuses.ONLINE,
            is_edited=False
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def update(self, *, db_obj: Posts, obj_in: PostUpdate) -> Posts:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def archive(self, *, id: int) -> Optional[Posts]:
        post = await self.get(id=id)
        if not post:
            return None

        setattr(post, "status", Statuses.ARCHIVED)
        setattr(post, "updated_at", datetime.utcnow())

        async with create_async_session() as session:
            session.add(post)
            await session.commit()
            await session.refresh(post)

            return post

    async def unarchive(self, *, id: int) -> Optional[Posts]:
        post = await self.get(id=id)
        if not post:
            return None

        setattr(post, "status", Statuses.ONLINE)
        setattr(post, "updated_at", datetime.utcnow())

        async with create_async_session() as session:
            session.add(post)
            await session.commit()
            await session.refresh(post)

            return post


post = CRUDPost(Posts)
