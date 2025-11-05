from src.services.base import BaseService
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_tasks


class FacilityService(BaseService):

    async def get_facilities(self):
        test_tasks.delay()
        return await self.db.facilities.get_all()

    async def create_facility(self, facility: FacilitiesAdd):
        facility = await self.db.facilities.add(facility)
        await self.db.commit()
        return facility
