from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from db.model_base import SqlAlchemyBase
from db.session import create_async_session
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy import delete

ModelType = TypeVar("ModelType", bound=SqlAlchemyBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, id: int) -> Optional[ModelType]:
        async with create_async_session() as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        async with create_async_session() as session:
            query = select(self.model).offset(skip).limit(limit).all()
            result = await session.execute(query)

            return result.scalars()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def update(self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        async with create_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            return db_obj
