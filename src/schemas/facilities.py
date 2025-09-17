from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str


class Facility(FacilitiesAdd):
    id: int
