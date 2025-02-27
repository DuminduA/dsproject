# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import workspace_credit_pb2 as workspace__credit__pb2


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


class WorkspaceCreditServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetWorkspaceCredit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkspaceCreditServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetWorkspaceCredit': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWorkspaceCredit,
                    request_deserializer=workspace__credit__pb2.WorkspaceCreditRequest.FromString,
                    response_serializer=workspace__credit__pb2.WorkspaceCreditResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'my_service.WorkspaceCredit', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkspaceCredit(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetWorkspaceCredit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/my_service.WorkspaceCredit/GetWorkspaceCredit',
            workspace__credit__pb2.WorkspaceCreditRequest.SerializeToString,
            workspace__credit__pb2.WorkspaceCreditResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
