import asyncio
from uuid import UUID
from bootstrap import JobQueue
from database import DbConnection
from shortid import ShortId
from webapi.webapi.config import AppSettings
from workspace import abstracts


async def run_bulksms_campaign(
    validated_data: abstracts.RunBulkSmsCampaign,
    db_conn: DbConnection,
    workspace: UUID,
    settings: AppSettings,
    queue: JobQueue,
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
            )
        )
        for contact in validated_data.contacts
    ]
    await asyncio.gather(*tasks)


async def send_bulksms_message(
    message_to: str,
    workspace_sid: str,
    bulksms_sid: str,
    contact_count: int,
    queue: JobQueue,
):
    # redis_conn = Redis.from_url(
    #     settings.redis_settings, decode_responses=True, encoding="utf-8"
    # )

    await queue.sales_call(
        "save_bulksms_campaign_info",
        bulksms_sid,
        workspace_sid,
        {
            "number": message_to,
            "status": "failed",
            "price": 0,
        },
        contact_count,
    )
