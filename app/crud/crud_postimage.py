from typing import List

from data.post_statuses import Statuses
from db.session import create_async_session
from models.posts import PostImages
from schemas.post import PostImageCreate, PostImageUpdate
from sqlalchemy.future import select

from crud.base import CRUDBase


class CRUDPostImage(CRUDBase[PostImages, PostImageCreate, PostImageUpdate]):
    async def create(self, *, obj_in: PostImageCreate) -> PostImages:
        db_obj = PostImages(
            post_id=obj_in.post_id,
            image_id=obj_in.image_id,
            order=obj_in.order
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def get_by_post_id(self, post_id: int) -> List[PostImages]:
        async with create_async_session() as session:
            query = select(PostImages).filter(
                PostImages.post_id == post_id).order_by("order")
            result = await session.execute(query)

            return result.scalars().all()


postimage = CRUDPostImage(PostImages)
