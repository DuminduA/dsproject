from uuid import UUID
from starlette.applications import Starlette
from dotenv import load_dotenv
from shortid import ShortId
from workspace import views
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint
import json
import typing

# load environment variables.
load_dotenv()


from bootstrap import (
    init_database,
)


from webapi.webapi import config
from webapi.webapi.middlewares import load_middlewares
import bootstrap

ROUTES = []


def create_app(settings) -> Starlette:
    db = init_database(settings)
    queue = bootstrap.init_queue(settings)
    broadcast = bootstrap.init_broadcaster(settings)
    _middlewares = load_middlewares(settings)
    app = Starlette(
        debug=settings.debug,
        routes=ROUTES,
        middleware=_middlewares,
        on_startup=[
            db.connect,
            queue.connect,
            broadcast.connect,
        ],
        on_shutdown=[db.disconnect, broadcast.disconnect],
    )
    app.state.settings = settings
    app.state.db = db
    app.state.queue = queue
    app.state.broadcast = broadcast
    return app


app = create_app(config.get_application_settings())


connected_websockets: set = set()

class WorkspaceCreditWebSocketEndpoint(WebSocketEndpoint):
    async def __call__(self, websocket: WebSocket):
        # Add the new WebSocket instance to the set of connected WebSockets
        connected_websockets.add(websocket)
        try:
            await self.listen_workspace_credit(websocket)
        finally:
            # Remove the WebSocket instance when the connection is closed
            connected_websockets.remove(websocket)
    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
    
    async def on_receive(self, websocket: WebSocket, data: str):
        try:
            payload = json.loads(data)
            if 'workspace_id' in payload:
                workspace_id = ShortId(payload['workspace_id']).uuid()
                await self.listen_workspace_credit(workspace_id, websocket)
        except json.JSONDecodeError:
            pass
    
    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        pass
    
    async def listen_workspace_credit(self, workspace_id: UUID, websocket: WebSocket):
        previous_credit = None
        credit_update = await views.get_workspace_credit(ShortId.with_uuid(workspace_id), app.state.db)
        if credit_update != previous_credit:
            await websocket.send_text(json.dumps({"credit": credit_update["credit"]}))
            previous_credit = credit_update


async def send_credit_update_to_websockets(credit_update: typing.Dict):
    print(len(connected_websockets))
    for websocket in connected_websockets:
        print("ran through here")
        await websocket.send_text(json.dumps(credit_update))

app.add_websocket_route("/ws", WorkspaceCreditWebSocketEndpoint)
