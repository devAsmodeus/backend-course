import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    argnames="room_id, date_from, date_to, status_code",
    argvalues=[
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-10", 200),
        (1, "2025-01-01", "2025-01-10", 500),
    ]
)
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    # room_id, *_ = await db.rooms.get_all()
    response = await authenticated_ac.post(
        url='bookings',
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    response_json = response.json()

    assert response.status_code == status_code
    if response.status_code == 200:
        assert response_json["message"] == "Complete"
        assert isinstance(response_json, dict)


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    argnames="room_id, date_from, date_to, booked_rooms",
    argvalues=[
        (1, "2025-01-01", "2025-01-10", 1),
        (1, "2025-01-01", "2025-01-10", 2),
        (1, "2025-01-01", "2025-01-10", 3),
    ]
)
async def test_add_and_get_my_bookings(
        room_id,
        date_from,
        date_to,
        booked_rooms,
        authenticated_ac,
        delete_all_bookings
):
    response = await authenticated_ac.post(
        url='bookings',
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == 200

    response = await authenticated_ac.get(
        url='/bookings/me',
    )
    assert response.status_code == 200
    assert len(response.json()) == booked_rooms
