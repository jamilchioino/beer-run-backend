from typing import Protocol

from pydantic import UUID4
from app.core.domain.models import Beer, Item, Order, Round, Stock


# Really funny python duck typing
class Repository(Protocol):
    def get_all_stock(self) -> Stock: ...

    def get_beer_from_stock(self, beer_id: UUID4) -> Beer | None: ...

    def put_stock(self, beer: Beer) -> Beer: ...

    def delete_stock(self, beer_id: UUID4) -> Beer | None: ...

    def create_order(self) -> Order: ...

    def get_order(self, order_id: UUID4) -> Order | None: ...

    def get_all_orders(self) -> list[Order]: ...

    def add_round_to_order(
        self, order_id: UUID4, items: list[Item]
    ) -> Order | None: ...

    def delete_round_from_order(
        self, order_id: UUID4, round_id: UUID4
    ) -> Round | None: ...

    def put_order(self, order: Order) -> Order: ...
