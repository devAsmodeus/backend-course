from src.services.base import BaseService
from src.schemas.facilities import FacilitiesAdd


class FacilityService(BaseService):

    async def create_facility(self, facility: FacilitiesAdd):
        facility = await self.db.facilities.add(facility)
        await self.db.commit()
        return facility
