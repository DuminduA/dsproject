from shortid import ShortId
from .repository import BulksmsRepository
from .models import Bulksms
import grpc
from uuid import UUID

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