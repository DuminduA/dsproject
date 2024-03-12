
from typing import Dict, List
from uuid import UUID

from shortid import ShortId

from pydantic import BaseModel


class RunBulkSmsCampaign(BaseModel):
    bulksms_id: UUID
    sender_number: str
    content: str
    contacts: List[Dict]
    workspace: UUID
    estimated_cost: float


class SendBulkSmsCampaignInfo(BaseModel):
    contact_data: Dict
    workspace: ShortId
    campaign_id: ShortId
