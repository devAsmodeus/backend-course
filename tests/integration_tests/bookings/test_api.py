import pytest


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
