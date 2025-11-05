from datetime import date

from fastapi import APIRouter, Query, Path, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException
)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2025-08-20"),
    date_to: date = Query(example="2025-09-10"),
    hotel_title: str | None = Query(default=None, description="Название отеля"),
    hotel_location: str | None = Query(default=None, description="Местоположение отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination=pagination,
        date_from=date_from,
        date_to=date_to,
        hotel_title=hotel_title,
        hotel_location=hotel_location,
    )


@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int = Path(description="Айди отеля"),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return {"message": "Complete"}


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": Example(
                **{
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель 5 звезд у моря",
                        "location": "Сочи ул. Пляжная 12",
                    },
                }
            ),
            "2": Example(
                **{
                    "summary": "Астрахань",
                    "value": {
                        "title": "Отель у бедуинов",
                        "location": "Пустырник ул. Сама 77",
                    },
                }
            ),
            "3": Example(
                **{
                    "summary": "Заславль",
                    "value": {
                        "title": "Придворный отель 2 звезды",
                        "location": "Ул. Космонавтов 91",
                    },
                }
            ),
        }
    ),
):
    new_hotel = await HotelService(db).add_hotel(hotel_data)
    return {"message": "Complete", "data": new_hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_data: HotelAdd,
    hotel_id: int = Path(description="Айди отеля"),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    await HotelService(db).edit_hotel(hotel_data, hotel_id)
    return {"message": "Complete"}


@router.patch("/{hotel_id}")
async def update_hotel(
    db: DBDep, hotel_data: HotelPatch, hotel_id: int = Path(description="Айди отеля")
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    await HotelService(db).update_hotel(hotel_data, hotel_id)
    return {"message": "Complete"}
