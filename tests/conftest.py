import json
import pytest

from httpx import AsyncClient, ASGITransport
from pathlib import Path

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


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def mock_hotels(setup_database):
    json_path = Path(__file__).parent / "mock_hotels.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel_data in json_data:
            hotel_data = HotelAdd(**hotel_data)
            await db.hotels.add(hotel_data)
        else:
            await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def mock_rooms(mock_hotels):
    json_path = Path(__file__).parent / "mock_rooms.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for room_data in json_data:
            room_data = RoomAdd(**room_data)
            await db.rooms.add(room_data)
        else:
            await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(mock_rooms):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        await client.post(
            url='/auth/register',
            json={
                "email": "cat@dog.com",
                "password": "12345678",
            }
        )
