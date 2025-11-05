from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства в номерах"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesAdd,
):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"message": "Complete", "data": facility}
