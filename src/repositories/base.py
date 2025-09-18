from sqlalchemy import select, insert, update, delete
from  pydantic import BaseModel

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_filtered(self, *filter_, **filter_by):
        query = (
            select(self.model)
            .filter(*filter_)
            .filter_by(**filter_by)
        )
        result = await self.db_session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model_)
            for model_ in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.db_session.execute(query)
        if (model_ := result.scalars().one_or_none()) is None:
            return None
        else:
            return self.mapper.map_to_domain_entity(model_)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.db_session.execute(add_data_stmt)
        model_ = result.scalars().one()
        return self.mapper.map_to_domain_entity(model_)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.db_session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        edit_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.db_session.execute(edit_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.db_session.execute(delete_stmt)
