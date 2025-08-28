from fastapi import APIRouter, Query, Path, Body
from fastapi.openapi.models import Example

from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(
    prefix="/hotels",
    tags=['Отели']
)


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        hotel_title: str | None = Query(default=None, description="Название отеля"),
        hotel_location: str | None = Query(default=None, description="Местоположение отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=hotel_title,
        location=hotel_location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel(
        hotel_id: int,
        db: DBDep,
):
    return await db.hotels.get_one_or_none(
        id=hotel_id
    )


@router.delete("/{hotel_id}")
async def delete_hotel(
        db: DBDep,
        hotel_id: int = Path(description="Айди отеля"),
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"message": "Complete"}


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"message": "Complete", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        db: DBDep,
        hotel_data: HotelAdd,
        hotel_id: int = Path(description="Айди отеля"),
):
    await db.hotels.edit(
        hotel_data,
        id=hotel_id
    )
    await db.commit()

    return {"message": "Complete"}


@router.patch("/{hotel_id}")
async def update_hotel(
        db: DBDep,
        hotel_data: HotelPatch,
        hotel_id: int = Path(description="Айди отеля")
):
    await db.hotels.edit(
        hotel_data,
        exclude_unset=True,
        id=hotel_id
    )
    await db.commit()

    return {"message": "Complete"}
