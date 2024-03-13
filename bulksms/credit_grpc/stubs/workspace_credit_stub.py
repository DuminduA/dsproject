from bulksms.credit_grpc.descriptors import (
    workspace_credit as workspace__credit__pb2,
)


class WorkspaceCreditStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetWorkspaceCredit = channel.unary_unary(
                '/my_service.WorkspaceCredit/GetWorkspaceCredit',
                request_serializer=workspace__credit__pb2.WorkspaceCreditRequest.SerializeToString,
                response_deserializer=workspace__credit__pb2.WorkspaceCreditResponse.FromString,
                )
