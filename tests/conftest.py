import json
import pytest

from typing import AsyncGenerator
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
async def db(check_test_mode) -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db_connection:
        yield db_connection


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode, db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def mock_hotels(setup_database, db):
    json_path = Path(__file__).parent / "mock_hotels.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    hotels_ = [HotelAdd.model_validate(hotel) for hotel in json_data]
    await db.hotels.add_bulk(hotels_)
    await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def mock_rooms(mock_hotels, db):
    json_path = Path(__file__).parent / "mock_rooms.json"
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    rooms_ = [RoomAdd.model_validate(hotel) for hotel in json_data]
    await db.rooms.add_bulk(rooms_)
    await db.commit()


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
