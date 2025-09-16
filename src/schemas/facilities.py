from pydantic import BaseModel


class FacilitiesAddRequest(BaseModel):
    title: str


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int
