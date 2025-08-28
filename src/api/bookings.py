from fastapi import APIRouter

from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование номеров"]
)


@router.get("")
async def get_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.bookings.get_filtered(
        user_id=user_id
    )


@router.post("")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingsAddRequest
):
    room = await db.rooms.get_one_or_none(
        id=booking_data.room_id
    )
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"message": "Complete", "data": booking}