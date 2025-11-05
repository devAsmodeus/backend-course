from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.services.base import BaseService
from src.exceptions import ObjectNotFoundException, RoomNotFoundException


class BookingService(BaseService):

    async def add_booking(self, user_id: int, booking_data: BookingsAddRequest):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex

        _booking_data = BookingsAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        booking = await self.db.bookings.add_booking(
            data=_booking_data,
            hotel_id=room.hotel_id,
        )
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)