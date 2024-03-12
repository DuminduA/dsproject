from pydantic import BaseModel
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
class ProductAbstract(BaseModel):
    name:str
    description:str
    price:int
    quantity:int=200
    # image:list = []

class DatabaseProductAbstract(BaseModel):
    id:uuid.UUID
    name:str
    description:str
    price:int
    quantity:int
    # image:list = []



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