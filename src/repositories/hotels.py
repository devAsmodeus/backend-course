from sqlalchemy import select, func

from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title: str | None,
            location: str | None,
            limit: int,
            offset: int
    ) -> list[Hotel]:
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
        result = await self.db_session.execute(query)
        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
