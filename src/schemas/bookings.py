from pydantic import BaseModel
from datetime import date


class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingsAdd):
    id: int
