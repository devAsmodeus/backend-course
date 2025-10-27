async def test_add_booking(db, authenticated_ac):
    room_id, *_ = await db.rooms.get_all()
    response = await authenticated_ac.post(
        url='bookings',
        json={
            "room_id": room_id.id,
            "date_from": "2025-01-01",
            "date_to": "2025-01-10",
        }
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["message"] == "Complete"
    assert isinstance(response_json, dict)
