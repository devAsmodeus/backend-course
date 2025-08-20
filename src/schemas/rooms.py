from pydantic import BaseModel
from typing import Optional


class RoomsAdd(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int
    hotel_id: int


class RoomsPATCH(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
