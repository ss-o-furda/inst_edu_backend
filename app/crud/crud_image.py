from db.session import create_async_session
from models.images import Images
from schemas.image import ImageCreate, ImageUpdate

from crud.base import CRUDBase


class CRUDImage(CRUDBase[Images, ImageCreate, ImageUpdate]):
    async def create(self, *, obj_in: ImageCreate) -> Images:
        db_obj = Images(
            image=obj_in.image,
            url=obj_in.url
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

image = CRUDImage(Images)
