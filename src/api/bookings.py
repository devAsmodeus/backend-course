from fastapi import APIRouter

from src.exceptions import (
    RoomCannotBeBookedException,
    AllRoomsAreBookedHTTPException
)
from src.schemas.bookings import BookingsAddRequest
from src.api.dependencies import UserIdDep, DBDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except RoomCannotBeBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"message": "Complete", "data": booking}
