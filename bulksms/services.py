from typing import Dict, List
from shortid import ShortId
from .repository import BulksmsRepository
from .models import Bulksms, BulksmsInfo
import grpc
from uuid import UUID
from loguru import logger

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
    
    async def update_bulksms_status(self,bulksms_id: UUID, status: str):
        bulksms = await self.bulksms_repository.update_bulksms_status(bulksms_id, status)
        if not bulksms:
            raise Exception("Bulksms doesn't exist.")
        return bulksms
    
    async def grpc_get_workspace_credit(self, workspace_id: UUID):
        from bulksms.credit_grpc import stubs, descriptors
        from bulksms.credit_grpc.stubs import workspace_credit_stub
        address = "localhost:8003"
        with grpc.insecure_channel(address) as channel:
            stub = workspace_credit_stub.WorkspaceCreditStub(channel)
            try:
                response = stub.GetWorkspaceCredit(
                    descriptors.workspace_credit.WorkspaceCreditRequest(
                        workspace_id=ShortId.with_uuid(workspace_id)
                    )
                )
                return float(response.workspace_credit)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    return None
                raise e
            
    async def add_bulksms_info_data(
        self,
        bulksms_id: UUID,
        workspace: UUID,
        contact: str,
        sms_status: str,
        price: float,
    ):
        try:
            saved_info = await self.bulksms_repository.get_bulksms_info_data(
                bulksms_id, contact
            )
            logger.warning(saved_info)
            if saved_info:
                info_data = await self.bulksms_repository.update_bulksms_info_data(
                    bulksms_id=bulksms_id,
                    sms_status=(
                        saved_info.sms_status
                        if saved_info.sms_status
                        in ["failed, delivered", "undelivered"]
                        else sms_status
                    ),
                    sms_cost=(
                        saved_info.sms_cost
                        if saved_info.sms_cost > 0
                        else price
                    )
                )
            else:
                saved_info = await self.bulksms_repository.get_bulksms_info_data(
                    bulksms_id, contact
                )
                if saved_info:
                    info_data = await self.bulksms_repository.update_bulksms_info_data(
                        bulksms_id=bulksms_id,
                        sms_status=(
                            saved_info.sms_status
                            if saved_info.sms_status
                            in ["failed, delivered", "undelivered"]
                            else sms_status
                        ),
                        sms_cost=(
                            saved_info.sms_cost
                            if saved_info.sms_cost > 0
                            else price
                        )
                    )
                else:
                    info_data = await self.bulksms_repository.add_bulksms_info_data(
                            bulksms_id=bulksms_id,
                            sms_status=sms_status,
                            contact_number=contact,
                            sms_cost=price,
                    )
            return info_data
        except:
            saved_info = await self.bulksms_repository.get_bulksms_info_data(
                bulksms_id, contact
            )
            logger.warning(saved_info)
            if saved_info:
                info_data = await self.bulksms_repository.update_bulksms_info_data(
                    bulksms_id=bulksms_id,
                    sms_status=(
                        saved_info.sms_status
                        if saved_info.sms_status
                        in ["failed, delivered", "undelivered"]
                        else sms_status
                    ),
                    sms_cost=(
                        saved_info.sms_cost
                        if saved_info.sms_cost > 0
                        else price
                    )
                )
            else:
                info_data = await self.bulksms_repository.add_bulksms_info_data(
                        bulksms_id=bulksms_id,
                        sms_status=sms_status,
                        contact_number=contact,
                        sms_cost=price,
                )
            return info_data 
        
    async def add_initial_bulksms_info_data(
        self,
        bulksms_id: UUID,
        contacts: List[Dict]
    ):
        await self.bulksms_repository.add_initial_campaign_data(
            bulksms_id=bulksms_id,
            contacts=contacts
        )

            
