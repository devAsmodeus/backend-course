from sqlalchemy import select, insert, update, delete
from  pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.db_session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.db_session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        edit_data_stmt = update(self.model).values(**data.model_dump()).filter_by(**filter_by)
        await self.db_session.execute(edit_data_stmt)

    async def delete(self, **filter_by) -> None:
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.db_session.execute(delete_data_stmt)
