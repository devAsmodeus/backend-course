async def test_get_hotels(ac):
    response = await ac.get(
        url='/hotels',
        params={
            "date_from": "2025-01-01",
            "date_to": "2025-01-10",
        }
    )
    print(f"{response=}")

    assert response.status_code == 200
