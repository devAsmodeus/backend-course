from sqlalchemy import select, func

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title: str | None,
            location: str | None,
            limit: int,
            offset: int
    ):
        query = select(HotelsOrm)
        if title:
            query = query.where(func.lower(HotelsOrm.title).contains(title.lower()))
        if location:
            query = query.where(func.lower(HotelsOrm.location).contains(location.lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.db_session.execute(query)
        hotels = result.scalars().all()
        return hotels
