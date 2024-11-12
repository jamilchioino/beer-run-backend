from typing import Optional, Tuple
from pydantic import UUID4

from app.core.domain.models import Beer, Item, Order, Round, Stock
from app.core.ports.driver import Driver
from app.core.ports.repository import Repository


class Service(Driver):
    def __init__(self, repository: Repository):
        self.repository: Repository = repository

    def get_stock_for_beer(self, beer_id: UUID4) -> Beer | None:
        return self.repository.get_beer_from_stock(beer_id)

    def get_all_stock(self) -> Stock:
        return self.repository.get_all_stock()

    def put_stock(self, beer: Beer) -> Beer:
        return self.repository.put_stock(beer)

    def delete_stock(self, beer_id: UUID4) -> Beer | None:
        return self.repository.delete_stock(beer_id)

    def create_order(self) -> Order:
        return self.repository.create_order()

    def get_order(self, order_id: UUID4) -> Order | None:
        order = self.repository.get_order(order_id)

        if order is None:
            return None

        # Join
        for round in order.rounds:
            for item in round.items:
                print("peer")
                item.beer = self.repository.get_beer_from_stock(beer_id=item.beer_id)

        return order

    def get_all_orders(self) -> list[Order]:
        orders = self.repository.get_all_orders()

        # Join
        for order in orders:
            for rounds in order.rounds:
                for item in rounds.items:
                    item.beer = self.repository.get_beer_from_stock(
                        beer_id=item.beer_id
                    )
        return orders

    def close_tab(self, order_id: UUID4) -> Tuple[Order | None, Optional[str]]:
        order = self.repository.get_order(order_id)

        if order is None:
            return None, "order not found"

        sub_total = 0.0
        discounts = 0.0

        for round in order.rounds:
            round_total_with_discounts = 0.0
            round_total_no_discounts = 0.0
            for item in round.items:
                round_total_with_discounts += (
                    (item.price_per_unit - item.discount_flat)
                    * item.quantity
                    * (1 - item.discount_rate)
                )
                round_total_no_discounts += item.price_per_unit * item.quantity
            sub_total += round_total_no_discounts
            discounts += round_total_no_discounts - round_total_with_discounts

        order.sub_total = sub_total
        order.discounts = discounts
        # TODO: avoid hardcoding taxes
        order.taxes = (sub_total - discounts) * 0.18
        order.total = sub_total - discounts + order.taxes
        order.paid = True

        self.repository.put_order(order)
        return order, None

    def add_round_to_order(
        self, order_id: UUID4, items: list[Item]
    ) -> Tuple[Order | None, Optional[str]]:
        # Get order to append a round on
        order = self.repository.get_order(order_id)
        if order is None:
            return None, "order not found"

        # Assemble transaction
        transaction: list[Item] = []

        for item in items:
            # Get beer stock
            beer = self.repository.get_beer_from_stock(item.beer_id)
            if beer is None:
                return None, "beer not found in stock"

            # Check there's enough stock
            if beer.quantity < item.quantity:
                return (
                    None,
                    f"not enough beer in stock: {beer.quantity} {beer.name}(s) left, {item.quantity} requested",
                )

            transaction.append(
                Item(
                    beer_id=beer.id,
                    price_per_unit=beer.price,
                    discount_flat=item.discount_flat,
                    discount_rate=item.discount_rate,
                    quantity=item.quantity,
                )
            )

            beer.quantity -= item.quantity
            self.repository.put_stock(beer)

        order = self.repository.add_round_to_order(order_id=order.id, items=transaction)

        return order, None

    def delete_round_from_order(self, order_id: UUID4, round_id: UUID4) -> Round | None:
        return self.repository.delete_round_from_order(
            order_id=order_id, round_id=round_id
        )
