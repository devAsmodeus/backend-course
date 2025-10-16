async def test_add_facilities(ac):
    facilities = ['Интернет', 'Солярий', 'Баня']
    for facility in facilities:
        response = await ac.post(
            url='/facilities',
            json={
                'title': facility,
            }
        )
        print(response.text)
        assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get(url='/facilities')
    print(f"{response.json()=}")
    assert response.status_code == 200
