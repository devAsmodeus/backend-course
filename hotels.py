from fastapi import APIRouter, Query, Path, Body

from schemas.hotels import Hotel, HotelPATCH


hotels = [
    {"id": 1, "title": "Dubai", "name": "Dubai"},
    {"id": 2, "title": "Sochi", "name": "Sochi"},
    {"id": 3, "title": "Minsk", "name": "Minsk"}
]


router = APIRouter(
    prefix="/hotels",
    tags=['Отели']
)


@router.get("")
async def get_hotels(
        hotel_id: int | None = Query(default=None, description="Айди отеля"),
        hotel_title: str | None = Query(default=None, description="Название отеля"),
        hotel_name: str | None = Query(default=None, description="Полное название отеля")
) -> list[dict]:
    result = list()
    for hotel in hotels:
        if hotel_id and hotel.get("id") != hotel_id:
            continue
        if hotel_title and hotel.get("title") != hotel_title:
            continue
        if hotel_name and hotel.get("name") != hotel_name:
            continue
        result.append(hotel)
    else:
        return result


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int = Path(description="Айди отеля")
) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"message": "Complete"}


@router.post("")
async def create_hotel(
        hotel_data: Hotel
) -> dict:
    global hotels
    hotels.append({
        "id": hotels[-1].get("id") + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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
