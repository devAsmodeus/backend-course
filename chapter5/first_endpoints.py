import uvicorn

from fastapi import FastAPI, Query, Path, Body
from fastapi.openapi.docs import get_swagger_ui_html


hotels = [
    {"id": 1, "title": "Dubai", "name": "Dubai"},
    {"id": 2, "title": "Sochi", "name": "Sochi"},
    {"id": 3, "title": "Minsk", "name": "Minsk"}
]

app = FastAPI(docs_url=None)


@app.get("/hotels")
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


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(
        hotel_id: int = Path(description="Айди отеля")
) -> dict:
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"message": "Complete"}


@app.post("/hotels")
async def create_hotel(
        hotel_title: str = Body(embed=True, description="Название отеля")
) -> dict:
    global hotels
    hotels.append({
        "id": hotels[-1].get("id") + 1,
        "title": hotel_title,
        "name": hotel_title
    })
    return {"message": "Complete"}


@app.put("/hotels/{hotel_id}")
async def edit_hotel(
        hotel_id: int = Path(description="Айди отеля"),
        hotel_title: str = Body(embed=True, description="Название отеля"),
        hotel_name: str = Body(embed=True, description="Полное название отеля")
):
    global hotels
    result = list()
    for hotel in hotels:
        if hotel.get("id") == hotel_id:
            result.append({
                "id": hotel_id,
                "title": hotel_title,
                "name": hotel_name
            })
        else:
            result.append(hotel)
    else:
        hotels = result
        return {"message": "Complete"}


@app.patch("/hotels/{hotel_id}")
async def update_hotel(
        hotel_id: int = Path(description="Айди отеля"),
        hotel_title: str | None = Body(default=None, embed=True, description="Название отеля"),
        hotel_name: str | None = Body(default=None, embed=True, description="Полное название отеля")
):
    if hotel_title and hotel_name:
        return {"message": "Forbidden"}
    else:
        global hotels
        result = list()
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                result.append({
                    "id": hotel_id,
                    "title": hotel_title if hotel_title else hotel.get("title"),
                    "name": hotel_name if hotel_name else hotel.get("name")
                })
            else:
                result.append(hotel)
        else:
            hotels = result
            return {"message": "Complete"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run('first_endpoints:app', reload=True)
