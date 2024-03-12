from starlette.routing import Route
from .route_handlers import create_bulksms


class BaseRoute:
    routes = []

class Routes(BaseRoute):
    routes = [
        Route('/', endpoint=create_bulksms, methods=['POST']),
    ]