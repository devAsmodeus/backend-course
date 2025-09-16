from fastapi import APIRouter

from src.schemas.facilities import FacilitiesAddRequest, FacilitiesAdd
from src.api.dependencies import DBDep


router = APIRouter(
    prefix="/facilities",
    tags=["Удобства в номерах"]
)


@router.get("")
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()


@router.post("")
async def add_facilities(
        db: DBDep,
        facilities_data: FacilitiesAddRequest,
):
    facilities = await db.facilities.add(
        facilities_data
    )
    await db.commit()

    return {"message": "Complete", "data": facilities}
