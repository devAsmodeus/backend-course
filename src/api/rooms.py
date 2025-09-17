from datetime import date
from fastapi import APIRouter, Path, Body, Query
from fastapi.openapi.models import Example

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep


router = APIRouter(
    prefix="/hotels",
    tags=['Номера']
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-08-20"),
        date_to: date = Query(example="2025-09-10"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    return await db.rooms.get_one_or_none(
        id=room_id,
        hotel_id=hotel_id,
    )


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id,
    )
    await db.commit()

    return {"message": "Complete"}


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
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
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
        for facility_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"message": "Complete", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        db: DBDep,
        room_data: RoomAddRequest,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        _room_data,
        id=room_id
    )
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id,
        facility_ids=room_data.facilities_ids
    )
    await db.commit()

    return {"message": "Complete"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room(
        db: DBDep,
        room_data: RoomPatchRequest,
        hotel_id: int = Path(description="Айди отеля"),
        room_id: int = Path(description="Айди комнаты"),
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        hotel_id=hotel_id,
        id=room_id
    )
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id,
            facility_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()

    return {"message": "Complete"}
