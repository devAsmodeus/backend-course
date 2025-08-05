from fastapi import APIRouter, Query, Path, Body
from fastapi.openapi.models import Example

from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm

from sqlalchemy import insert, select


router = APIRouter(
    prefix="/hotels",
    tags=['Отели']
)


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        hotel_id: int | None = Query(default=None, description="Айди отеля"),
        hotel_title: str | None = Query(default=None, description="Название отеля"),
        hotel_name: str | None = Query(default=None, description="Полное название отеля"),
):
    async with async_session_maker() as db_session:
        query = select(HotelsOrm)
        result = await db_session.execute(query)
        hotels_ = result.scalars().all()
        return hotels_

    # return hotels_[pagination.per_page*(pagination.page-1):pagination.per_page*pagination.page]


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
) -> dict:
    async with async_session_maker() as db_session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await db_session.execute(add_hotel_stmt)
        await db_session.commit()

    return {"message": "Complete"}


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
