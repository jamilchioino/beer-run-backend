from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import UUID4, BaseModel


class Beer(BaseModel):
    id: UUID4 = uuid4()
    name: str = ""
    price: float = 0
    quantity: int = 0


class Stock(BaseModel):
    lastUpdated: datetime | None = None
    beers: List[Beer] = []


class Item(BaseModel):
    beer_id: UUID4 = uuid4()
    # Price at this specific point in time
    # mitigates price discrepancies if beer price
    # is changed in the future and/or in between rounds
    price_per_unit: float = 0
    quantity: int = 1
    # Flat discount (10$ Less)
    discount_flat: float = 0
    # Flat rate (10% off)
    discount_rate: float = 0


class Round(BaseModel):
    id: UUID4 = uuid4()
    created: datetime = datetime.now()
    items: List[Item] = []


class Order(BaseModel):
    id: UUID4 = uuid4()
    created: datetime = datetime.now()
    paid: bool = False
    sub_total: float = 0
    taxes: float = 0
    discounts: float = 0
    total: float = 0
    rounds: List[Round] = []
