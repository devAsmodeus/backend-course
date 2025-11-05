import pytest


@pytest.mark.parametrize(
    argnames=["email", "password", "status_code"],
    argvalues=[
        ('catpac@dog.com', '12345678', 200),
        ('catpac@dag.com', '123456', 200),
        ('catpac@dag.com', '123456', 409),
        ('cat', '123456', 422),
    ]
)
async def test_auth_flow(
        email,
        password,
        status_code,
        ac
):
    resp_reg = await ac.post(
        url='/auth/register',
        json={
            "email": email,
            "password": password,
        }
    )
    assert resp_reg.status_code == status_code
    if resp_reg.status_code != 200:
        return

    resp_log = await ac.post(
        url='/auth/login',
        json={
            "email": email,
            "password": password,
        }
    )
    assert resp_log.status_code == 200
    assert ac.cookies['access_token'] is not None
    assert resp_log.json()['access_token'] is not None

    resp_me = await ac.get('/auth/me')
    assert resp_me.status_code == 200
    user_data = resp_me.json()
    assert user_data['email'] == email
    assert "id" in user_data
    assert "password" not in user_data
    assert "hashed_password" not in user_data

    resp_log = await ac.post('/auth/logout')
    assert resp_log.status_code == 200
    assert 'access_token' not in ac.cookies
