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
    new_booking_data = await db.bookings.add(booking_data)
    print(f"{new_booking_data=}")
    await db.commit()


# async def test_read_booking(db):
#     room_id, *_ = await db.rooms.get_all()
#     user_id, *_ = await db.users.get_all()
#
#     booking = await db.bookings.get_one_or_none(
#         room_id=room_id.id,
#         user_id=user_id.id
#     )
#
#     assert booking
#     assert booking is not None


# async def test_update_booking(db):
#     room_id, *_ = await db.rooms.get_all()
#     user_id, *_ = await db.users.get_all()
#     booking_data = BookingsAdd(
#         room_id=room_id.id,
#         user_id=user_id.id,
#         date_from=date(2025, 1, 1),
#         date_to=date(2025, 12, 31),
#         price=10_000,
#     )
#     new_booking_data = await db.bookings.add(booking_data)
#     print(f"{new_booking_data=}")
#     await db.commit()
#
#
# async def test_delete_booking(db):
#     room_id, *_ = await db.rooms.get_all()
#     user_id, *_ = await db.users.get_all()
#     booking_data = BookingsAdd(
#         room_id=room_id.id,
#         user_id=user_id.id,
#         date_from=date(2025, 1, 1),
#         date_to=date(2025, 12, 31),
#         price=10_000,
#     )
#     new_booking_data = await db.bookings.add(booking_data)
#     print(f"{new_booking_data=}")
#     await db.commit()
