from typing import List, Optional

from core.security import get_password_hash, verify_password
from db.session import create_async_session
from models.users import Users
from schemas.user import UserChangePassword, UserCreate, UserUpdate
from sqlalchemy.future import select

from crud.base import CRUDBase


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    async def create(self, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            full_name=obj_in.full_name,
            user_name=obj_in.user_name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            sex=obj_in.sex,
            birth_date=obj_in.birth_date,
            web_site=obj_in.web_site,
            bio=obj_in.bio
        )

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def update(self, *, db_obj: Users, obj_in: UserUpdate) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def get_by_email(self, *, email: str) -> Optional[Users]:
        async with create_async_session() as session:
            query = select(Users).filter(Users.email == email)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def get_by_username(self, *, username: str) -> Optional[Users]:
        async with create_async_session() as session:
            query = select(Users).filter(Users.user_name == username)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def search_by_username(self, search_query: str) -> List[Users]:
        async with create_async_session() as session:
            query = select(Users).filter(
                Users.user_name.contains(search_query))  # type: ignore
            result = await session.execute(query)

            return result.scalars().all()

    async def change_password(self, *, db_obj: Users, obj_in: UserChangePassword) -> Users:
        setattr(db_obj, "hashed_password", get_password_hash(obj_in.new_password))

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def authenticate(self, *, username: str, password: str) -> Optional[Users]:
        if "@" in username:
            user = await self.get_by_email(email=username)
        else:
            user = await self.get_by_username(username=username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def is_active(self, user: Users) -> bool:
        return user.is_active

    def is_superuser(self, user: Users) -> bool:
        return user.is_superuser


user = CRUDUser(Users)
