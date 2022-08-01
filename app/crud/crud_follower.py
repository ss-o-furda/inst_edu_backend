from db.session import create_async_session
from models.users import Followers
from schemas.follower import FollowerCreate, FollowerUpdate
from sqlalchemy.future import select
from sqlalchemy import func


from crud.base import CRUDBase


class CRUDFollower(CRUDBase[Followers, FollowerCreate, FollowerUpdate]):
    async def create(self, *, obj_in: FollowerCreate) -> Followers:
        db_obj = Followers(
            follow_id=obj_in.follow_id,
            follower_id=obj_in.follower_id
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def get_user_followers(self, user_id: int) -> Followers:
        async with create_async_session() as session:
            query = select(Followers).filter(Followers.follow_id == user_id)
            result = await session.execute(query)

            return result.scalars().all()

    async def get_user_follows(self, user_id: int) -> Followers:
        async with create_async_session() as session:
            query = select(Followers).filter(Followers.follower_id == user_id)
            result = await session.execute(query)

            return result.scalars().all()

    async def get_user_followers_count(self, user_id: int) -> int:
        async with create_async_session() as session:
            query = select(func.count()).filter(Followers.follow_id == user_id)
            result = await session.execute(query)

            return result.scalar()

    async def get_user_follows_count(self, user_id: int) -> int:
        async with create_async_session() as session:
            query = select(func.count()).filter(
                Followers.follower_id == user_id)
            result = await session.execute(query)

            return result.scalar()

    async def is_me_follow(self, user_id: int, me_id: int) -> bool:
        async with create_async_session() as session:
            query = select(Followers).filter(Followers.follow_id ==
                                             me_id).filter(Followers.follower_id == user_id)
            result = await session.execute(query)

            return bool(result.scalar_one_or_none())

    async def get_current_follow(self, user_id: int, me_id: int) -> Followers:
        async with create_async_session() as session:
            query = select(Followers).filter(Followers.follow_id ==
                                             me_id).filter(Followers.follower_id == user_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def delete(self, id: int) -> None:
        async with create_async_session() as session:
            res = await self.get(id=id)
            if res:
                await session.delete(res)
                await session.commit()


follower = CRUDFollower(Followers)
