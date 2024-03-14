import asyncio
import random
import time
import typing
from uuid import UUID
from bootstrap import JobQueue
from database import DbConnection
from krispbroadcaster import KrispBroadcast
from shortid import ShortId
from webapi.webapi.config import AppSettings
from webapi.webapi.main import send_credit_update_to_websockets
from workspace import abstracts
from workspace.views import deduct_credit


async def run_bulksms_campaign(
    validated_data: abstracts.RunBulkSmsCampaign,
    db_conn: DbConnection,
    workspace: UUID,
    settings: AppSettings,
    queue: JobQueue,
    broadcaster: KrispBroadcast
):
    """Sends bulk messages via messaging service"""
    workspace_sid = ShortId.with_uuid(workspace)
    bulksms_id = validated_data.bulksms_id
    contact_count = len(validated_data.contacts)
    tasks = [
        asyncio.create_task(
            send_bulksms_message(
                message_to=contact["contact_number"],
                workspace_sid=workspace_sid,
                bulksms_sid=bulksms_id,
                contact_count=contact_count,
                queue=queue,
                db_conn=db_conn,
                broadcaster=broadcaster
            )
        )
        for contact in validated_data.contacts
    ]
    await asyncio.gather(*tasks)


# from datetime import datetime

# def uuid_convert(o):
#     if isinstance(o, UUID):
#         return o.hex
#     if isinstance(o, datetime):
#         return o.isoformat()
    

# import json
# def serialize_message(message):
#     # uuid_convert is required coz UUID is not JSON serializable
#     dump = json.dumps(message, default=uuid_convert)
#     return dump


# def deserialize_message(message):
#     return json.loads(message)

# async def publish_workspace_credit(
#     workspace: typing.List[UUID],
#     message: typing.Dict,
#     broadcast: KrispBroadcast,
# ) -> None:
#     payload = message
#     await broadcast.publish(
#         channel=workspace.hex,
#         message=serialize_message(dict(event="workspace_credit", message=payload)),
#     )

# async def workspace_credit_updates(
#     workspaces: typing.List[UUID], broadcast: KrispBroadcast
# ) -> typing.AsyncGenerator:
#     async with broadcast.subscribe(channel=workspaces) as subscriber:
#         print(subscriber, workspaces, "*********************************8")
#         async for event in subscriber:
#             print("reached heer")
#             print(event, "************************************************8")
#             yield deserialize_message(event.message)


async def send_bulksms_message(
    message_to: str,
    workspace_sid: str,
    bulksms_sid: str,
    contact_count: int,
    queue: JobQueue,
    db_conn: DbConnection,
    broadcaster: KrispBroadcast
):
    # redis_conn = Redis.from_url(
    #     settings.redis_settings, decode_responses=True, encoding="utf-8"
    # )
    for each in ["queued", "sent", "delivered"]:
        defer_by_seconds = random.uniform(5, 10)
        await queue.sales_call(
            "save_bulksms_campaign_info",
            bulksms_sid,
            workspace_sid,
            {
                "number": message_to,
                "status": each,
                "price": 0.1,
            },
            contact_count,
            defer_by_seconds=defer_by_seconds
        )
        if each == 'sent':
            print("reached_here")
            credit = await deduct_credit(workspace_id=ShortId.uuid(workspace_sid), db_conn=db_conn)
            await send_credit_update_to_websockets(credit_update=credit)
