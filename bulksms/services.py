from .repository import BulksmsRepository
from .models import Bulksms

class BulksmsServices:
    def __init__(self, db):
        self.bulksms_repository = BulksmsRepository(db)
    
    async def get_all_bulksms(self):
        return await self.bulksms_repository.get_all_bulksmss()
    
    async def get_bulksms_by_id(self, bulksms_id:str):
        return await self.bulksms_repository.get_bulksms_by_id(bulksms_id)
    
    async def create_bulksms(self, data:Bulksms):
        bulksms = await self.bulksms_repository.create_bulksms(data)
        if not bulksms:
            raise Exception("Bulksms doesn't exist.")
        return bulksms