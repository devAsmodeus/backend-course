from fastapi import APIRouter, Path, Body
from fastapi.openapi.models import Example

from src.schemas.rooms import RoomsPATCH, RoomsAdd
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository


router = APIRouter(
    prefix="/hotels",
    tags=['Номера']
)


@router.get("/{hotel_id}/rooms")
async def get_hotels(
        hotel_id: int,
):
    async with async_session_maker() as db_session:
        return await RoomsRepository(db_session).get_all(
            hotel_id=hotel_id,
        )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_hotel(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as db_session:
        return await RoomsRepository(db_session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(
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
async def create_hotel(
        hotel_data: RoomsAdd = Body(openapi_examples={
            "1": Example(**{
                "summary": "Сочи",
                "value": {
                    "hotel_id": 11,
                    "title": "Номер для одного",
                    "description": 'None',
                    "price": 9_000,
                    "quantity": 1
                }
            }),
            "2": Example(**{
                "summary": "Астрахань",
                "value": {
                    "hotel_id": 11,
                    "title": "Номер для двоих",
                    "description": "Большая комната с двухместной кроватью",
                    "price": 15_000,
                    "quantity": 1
                }
            }),
            "3": Example(**{
                "summary": "Заславль",
                "value": {
                    "hotel_id": 1,
                    "title": "Номер морской вид",
                    "description": "Красивый вид на море",
                    "price": 23_000,
                    "quantity": 1
                }
            }),
        })
):
    async with async_session_maker() as db_session:
        room = await RoomsRepository(db_session).add(hotel_data)
        await db_session.commit()

    return {"message": "Complete", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_hotel(
        hotel_data: RoomsAdd,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    async with async_session_maker() as db_session:
        await RoomsRepository(db_session).edit(
            hotel_data,
            hotel_id=hotel_id,
            id=room_id
        )
        await db_session.commit()

    return {"message": "Complete"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_hotel(
        hotel_data: RoomsPATCH,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    async with async_session_maker() as db_session:
        await RoomsRepository(db_session).edit(
            hotel_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id
        )
        await db_session.commit()

    return {"message": "Complete"}
