from pydantic import BaseModel
from typing import Optional


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
