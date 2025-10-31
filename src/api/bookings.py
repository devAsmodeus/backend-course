from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, RoomCannotBeBookedException
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingsAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Room not found")

    _booking_data = BookingsAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(
            data=_booking_data,
            hotel_id=room.hotel_id,
        )
    except RoomCannotBeBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()
    return {"message": "Complete", "data": booking}
