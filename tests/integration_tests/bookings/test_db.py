from datetime import date

from src.schemas.bookings import BookingsAdd


async def test_create_booking(db):
    room_id, *_ = await db.rooms.get_all()
    user_id, *_ = await db.users.get_all()
    booking_data = BookingsAdd(
        room_id=room_id.id,
        user_id=user_id.id,
        date_from=date(2025, 1, 1),
        date_to=date(2025, 12, 31),
        price=10_000,
    )
    new_booking = await db.bookings.add(booking_data)
    print(f"{new_booking=}")

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    # а еще можно вот так разом сравнить все параметры
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # обновить бронь
    updated_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingsAdd(
        user_id=user_id.id,
        room_id=room_id.id,
        date_from=date(year=2024, month=8, day=10),
        date_to=updated_date,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
