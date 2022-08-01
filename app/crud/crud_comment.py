from re import S
from typing import List
from unittest import result
from db.session import create_async_session
from models.comments import Comments, Replies
from schemas.comment import CommentCreate, CommentUpdate
from sqlalchemy.future import select

from crud.base import CRUDBase


class CRUDComment(CRUDBase[Comments, CommentCreate, CommentUpdate]):
    async def get_by_post_id(self, post_id: int) -> List[Comments]:
        async with create_async_session() as session:
            query = select(Comments).filter(Comments.post_id == post_id)
            result = await session.execute(query)

            return result.scalars().all()

    async def create(self, *, obj_in: CommentCreate) -> Comments:
        db_obj = Comments(
            comment=obj_in.comment,
            post_id=obj_in.post_id,
            user_id=obj_in.user_id,
            is_edited=False
        )
        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def update(self, *, db_obj: Comments, obj_in: CommentUpdate) -> Comments:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def delete(self, id: int) -> None:
        async with create_async_session() as session:
            comment = await self.get(id=id)
            if comment:
                await session.delete(comment)
                await session.commit()


comment = CRUDComment(Comments)
