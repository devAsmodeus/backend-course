from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(
        title='Some new hotel Dubai Marina 7 stars WOW!',
        location='Somewhere near where Dubai Marina'
    )
    new_hotel_data = await db.hotels.add(hotel_data)
    print(f"{new_hotel_data=}")
    await db.commit()