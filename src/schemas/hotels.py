from pydantic import BaseModel
from typing import Optional


class Hotel(BaseModel):
    title: str
    name: str


class HotelPATCH(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
