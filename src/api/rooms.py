from fastapi import APIRouter, Path, Body
from fastapi.openapi.models import Example

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository


router = APIRouter(
    prefix="/hotels",
    tags=['Номера']
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
):
    async with async_session_maker() as db_session:
        return await RoomsRepository(db_session).get_filtered(
            hotel_id=hotel_id,
        )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as db_session:
        return await RoomsRepository(db_session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    async with async_session_maker() as db_session:
        await RoomsRepository(db_session).delete(
            id=room_id,
            hotel_id=hotel_id,
        )
        await db_session.commit()

    return {"message": "Complete"}


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": Example(**{
                "summary": "Сочи",
                "value": {
                    "title": "Номер для одного",
                    "price": 9_000,
                    "quantity": 1
                }
            }),
            "2": Example(**{
                "summary": "Астрахань",
                "value": {
                    "title": "Номер для двоих",
                    "description": "Большая комната с двухместной кроватью",
                    "price": 15_000,
                    "quantity": 1
                }
            }),
            "3": Example(**{
                "summary": "Заславль",
                "value": {
                    "title": "Номер морской вид",
                    "description": "Красивый вид на море",
                    "price": 23_000,
                    "quantity": 1
                }
            }),
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as db_session:
        room = await RoomsRepository(db_session).add(_room_data)
        await db_session.commit()

    return {"message": "Complete", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        room_data: RoomAddRequest,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as db_session:
        await RoomsRepository(db_session).edit(
            _room_data,
            id=room_id
        )
        await db_session.commit()

    return {"message": "Complete"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(
        room_data: RoomPatchRequest,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as db_session:
        await RoomsRepository(db_session).edit(
            _room_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id
        )
        await db_session.commit()

    return {"message": "Complete"}
