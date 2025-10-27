import json
import pytest

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from pathlib import Path

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.utils.db_manager import DBManager
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    json_path = Path(__file__).parent / "mock_rooms.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        rooms_data = json.load(json_file)

    json_path = Path(__file__).parent / "mock_hotels.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        hotels_data = json.load(json_file)

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        hotels_ = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
        await db_.hotels.add_bulk(hotels_)

        rooms_ = [RoomAdd.model_validate(hotel) for hotel in rooms_data]
        await db_.rooms.add_bulk(rooms_)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        url='/auth/register',
        json={
            "email": "cat@dog.com",
            "password": "12345678",
        }
    )


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        url='/auth/login',
        json={
            "email": "cat@dog.com",
            "password": "12345678",
        }
    )

    assert response.status_code == 200
    assert response.cookies
    assert 'access_token' in response.cookies

    yield ac
