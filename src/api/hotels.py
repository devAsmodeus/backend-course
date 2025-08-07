from fastapi import APIRouter, Query, Path, Body
from fastapi.openapi.models import Example

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm

from sqlalchemy import insert, select, func
from src.repositories.hotels import HotelsRepository


router = APIRouter(
    prefix="/hotels",
    tags=['Отели']
)


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        hotel_title: str | None = Query(default=None, description="Название отеля"),
        hotel_location: str | None = Query(default=None, description="Местоположение отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as db_session:
        return await HotelsRepository(db_session).get_all(
            title=hotel_title,
            location=hotel_location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int = Path(description="Айди отеля")
) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"message": "Complete"}


@router.post("")
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": Example(**{
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи ул. Пляжная 12"
                }
            }),
            "2": Example(**{
                "summary": "Астрахань",
                "value": {
                    "title": "Отель у бедуинов",
                    "location": "Пустырник ул. Сама 77"
                }
            }),
            "3": Example(**{
                "summary": "Заславль",
                "value": {
                    "title": "Придворный отель 2 звезды",
                    "location": "Ул. Космонавтов 91"
                }
            }),
        })
):
    async with async_session_maker() as db_session:
        hotel = await HotelsRepository(db_session).add(hotel_data)
        await db_session.commit()

    return {"message": "Complete", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_data: Hotel,
        hotel_id: int = Path(description="Айди отеля"),
):
    global hotels
    result = list()
    for hotel in hotels:
        if hotel.get("id") == hotel_id:
            result.append({
                "id": hotel_id,
                "title": hotel_data.title,
                "name": hotel_data.name
            })
        else:
            result.append(hotel)
    else:
        hotels = result
        return {"message": "Complete"}


@router.patch("/{hotel_id}")
async def update_hotel(
        hotel_data: HotelPATCH,
        hotel_id: int = Path(description="Айди отеля")
):
    if hotel_data.title and hotel_data.name:
        return {"message": "Forbidden"}
    else:
        global hotels
        result = list()
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                result.append({
                    "id": hotel_id,
                    "title": hotel_data.title if hotel_data.title else hotel.get("title"),
                    "name": hotel_data.name if hotel_data.name else hotel.get("name")
                })
            else:
                result.append(hotel)
        else:
            hotels = result
            return {"message": "Complete"}
