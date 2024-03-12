from pydantic import BaseModel, Json
from uuid import UUID
from datetime import datetime

# class CartAbstract(BaseModel):
#     user_id: UUID
#     status: CartStatusEnum = CartStatusEnum.ACTIVE
#     ordered_at: datetime = datetime.now()

# class DbCartItemAbstract(BaseModel):
#     id: UUID
#     cart_id: UUID
#     product_id: UUID
#     quantity: int = 1

# class CartItemAbstract(BaseModel):
#     cart_id: UUID
#     product_id: UUID
#     quantity: str

# class DbCartItemsAbstract(BaseModel):
#     id: UUID
#     cart_id: UUID
#     product_id: UUID
#     quantity: int = 1


from pydantic import BaseModel
import uuid
import typing 
from typing import List, Dict
from shortid import ShortId
class SendBulkSms(BaseModel):
    content: str
    # sender_number: str
    contacts: List[Dict]
    workspace: ShortId
    bulksms_id: ShortId
    # estimated_cost: float


class BulksmsAbstract(BaseModel):
    id: UUID = uuid.uuid4()
    workspace_id: UUID
    name: str
    status: str
    message: str
    total_cost: float = 0.0
    # estimated_cost: float = 0.0
    contact_count: int = 0
    created_at: datetime = datetime.now()
    modified_at: datetime = datetime.now()
    all_contacts: list = None


class UpdateBulksmsStatus(BaseModel):
    id: UUID = uuid.uuid4()
    status: str
    modified_at: datetime = datetime.now()


class BulksmsInfoAbstract(BaseModel):
    id: UUID = uuid.uuid4()
    sms_status: str
    sms_cost: float
    contact_name: str
    contact_number: str
    created_at: datetime = datetime.now()
    modified_at: datetime = datetime.now()
    modified_at: datetime = datetime.now()


class DbBulksmsAbstract(BaseModel):
    id: UUID
    workspace_id: UUID
    campaign_name: str
    status: str
    message: str
    total_cost: float = 0.0
    # estimated_cost: float = 0.0
    # contact_count: int = 0
    # created_at: datetime = datetime.now()