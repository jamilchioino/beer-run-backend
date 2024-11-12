from uuid import uuid4
from pydantic import UUID4, BaseModel

from app.core.domain.models import Order


# Models used by http
class Item(BaseModel):
    beer_id: UUID4 = uuid4()
    quantity: int = 0
    discount_flat: float = 0
    discount_rate: float = 0


class ItemRequest(BaseModel):
    items: list[Item]


class OrdersResponse(BaseModel):
    orders: list[Order]
