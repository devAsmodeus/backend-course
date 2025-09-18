from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomsWithRels
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.db_session.execute(query)
        return [
            RoomsWithRels.model_validate(model_, from_attributes=True)
            for model_ in result.unique().scalars().all()
        ]