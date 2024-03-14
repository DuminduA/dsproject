"""
"""


import logging
from uuid import UUID



from shortid import ShortId



from starlette.requests import Request

from redis import Redis

from workspace import abstracts, services

twilio_logger = logging.getLogger("twilio")
payment_logger = logging.getLogger("service")


async def run_bulksms_campaign(
    ctx, validated_data: abstracts.RunBulkSmsCampaign
):
    db_conn = ctx["db"]
    workspace_id = ShortId(validated_data.workspace).uuid()
    settings = ctx["settings"]
    await services.run_bulksms_campaign(
        validated_data,
        db_conn,
        workspace_id,
        settings,
        ctx["queue"],
        ctx["broadcaster"]
    )


