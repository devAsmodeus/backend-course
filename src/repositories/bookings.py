from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.db_session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]
