from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_tasks


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства в номерах"]
)


@router.get("")
@cache(expire=10)
async def get_facilities(
        db: DBDep,
):
    test_tasks.delay()
    return await db.facilities.get_all()


@router.post("")
async def create_facility(
        db: DBDep,
        facility_data: FacilitiesAdd,
):
    facility = await db.facilities.add(
        facility_data
    )
    await db.commit()

    return {"message": "Complete", "data": facility}
