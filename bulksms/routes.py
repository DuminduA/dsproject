from starlette.routing import Route
from .route_handlers import create_bulksms, run_bulksms


class BaseRoute:
    routes = []

class Routes(BaseRoute):
    routes = [
        Route('/create/', endpoint=create_bulksms, methods=['POST']),
        Route('/run/', endpoint=run_bulksms, methods=['POST']),
    ]