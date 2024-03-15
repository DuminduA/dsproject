from typing import Dict
from uuid import UUID

from shortid import ShortId

from bulksms import services
import logging
from loguru import logger

from system_stats import collect_system_stats, plot_system_stats


async def save_bulksms_campaign_info(
    ctx,
    bulksms_id: ShortId,
    workspace: ShortId,
    contact_data: Dict,
    total_contacts: int = 0,
):
    bulksms_id = ShortId(bulksms_id).uuid()
    bulksms_service = services.BulksmsServices(ctx['db'])
    await bulksms_service.add_bulksms_info_data(
        bulksms_id=bulksms_id,
        contact=contact_data["number"],
        sms_status=contact_data["status"],
        # sms_id=contact_data.get("sms_id", None),
        price=contact_data["price"],
        workspace=ShortId(workspace).uuid(),
    )
    bulksms = await bulksms_service.get_bulksms_by_id(bulksms_id=bulksms_id)
    status = bulksms["status"]
    logger.warning(
        f"campaign_status {status} queue handler {bulksms_id}",
    )
    if status == "completed":
        await bulksms_service.update_bulksms_status(
            bulksms_id=bulksms_id,
            status='completed'
        )


async def generate_system_stat(
    ctx,
    duration_seconds: int,
    contact_count: int
):
    cpu_usage_5_contacts, memory_usage_5_contacts = collect_system_stats(duration_seconds)
    plot_system_stats(cpu_usage_5_contacts, memory_usage_5_contacts, f"API with {contact_count} Contacts")
