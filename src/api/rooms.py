from datetime import date
from fastapi import APIRouter, Path, Body, Query
from fastapi.openapi.models import Example

from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    HotelNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-08-20"),
    date_to: date = Query(example="2025-09-10"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int = Path(description="Айди отеля"),
    room_id: int = Path(description="Айди комнаты"),
):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"message": "Complete"}


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": Example(
                **{
                    "summary": "Сочи",
                    "value": {
                        "title": "Номер для одного",
                        "price": 9_000,
                        "quantity": 1,
                    },
                }
            ),
            "2": Example(
                **{
                    "summary": "Астрахань",
                    "value": {
                        "title": "Номер для двоих",
                        "description": "Большая комната с двухместной кроватью",
                        "price": 15_000,
                        "quantity": 1,
                    },
                }
            ),
            "3": Example(
                **{
                    "summary": "Заславль",
                    "value": {
                        "title": "Номер морской вид",
                        "description": "Красивый вид на море",
                        "price": 23_000,
                        "quantity": 1,
                    },
                }
            ),
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"message": "Complete", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    room_data: RoomAddRequest,
    hotel_id: int = Path(description="Айди отеля"),
    room_id: int = Path(description="Айди комнаты"),
):
    await RoomService(db).edit_room(room_data, hotel_id, room_id)
    return {"message": "Complete"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(
    db: DBDep,
    room_data: RoomPatchRequest,
    hotel_id: int = Path(description="Айди отеля"),
    room_id: int = Path(description="Айди комнаты"),
):
    await RoomService(db).update_room(room_data, hotel_id, room_id)
    return {"message": "Complete"}
