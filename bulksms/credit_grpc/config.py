import os


def get_grpc_channel_address() -> str:
    # return "localhost:8003"
    if os.getenv("app_env") == "development":
        return "localhost:8003"
    return "krispcall-grpc-service:8003"
