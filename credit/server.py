from credit import workspace_credit_pb2, workspace_credit_pb2_grpc
from database import DbConnection


class WorkspaceCredit(workspace_credit_pb2_grpc.WorkspaceCreditServicer):
    def __init__(self, db_conn: DbConnection) -> None:
        self.db_conn = db_conn

    async def GetWorkspaceCredit(self, request, context):
        # workspace_id = ShortId(request.workspace_id).uuid()
        workspace_id = request.workspace_id

        # workspace_credit = await get_workspace_credit(
        #     workspace_id=workspace_id, db_conn=self.db_conn
        # )
        workspace_credit = 10

        return workspace_credit_pb2.WorkspaceCreditResponse(
            workspace_credit=workspace_credit
        )
