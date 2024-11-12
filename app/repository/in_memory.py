from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from app.core.domain.models import Beer, Item, Order, Round, Stock
from app.core.ports.ports import Repository

# Imagine this is a kv store or dictionary and not doing o(n) on every query


class InMemory(Repository):
    def __init__(self) -> None:
        self.stock: Stock = Stock()
        self.orders: list[Order] = []
        self.seed()

    # Hardcode seed data
    def seed(self) -> None:
        self.put_stock(Beer(name="Corona", price=100, quantity=5))
        self.put_stock(Beer(name="Modelo", price=200, quantity=10))
        self.put_stock(Beer(name="Pilsen", price=300, quantity=8))

    def get_all_stock(self) -> Stock:
        return self.stock

    def get_beer_from_stock(self, beer_id: UUID4) -> Beer | None:
        for stock_beer in self.stock.beers:
            if stock_beer.id == beer_id:
                return stock_beer

        return None

    def put_stock(self, beer: Beer) -> Beer:
        for i, stock_beer in enumerate(self.stock.beers):
            if stock_beer.id == beer.id:
                self.stock.beers[i] = beer
                return beer

        beer.id = uuid4()
        self.stock.beers.append(beer)
        self.stock.lastUpdated = datetime.now()

        return beer

    def delete_stock(self, beer_id: UUID4) -> Beer | None:
        for i, stock_beer in enumerate(self.stock.beers):
            if stock_beer.id == beer_id:
                del self.stock.beers[i]
                return stock_beer

        return None

    def create_order(self) -> Order:
        order = Order(created=datetime.now(), id=uuid4())
        self.orders.append(order)
        return order

    def get_order(self, order_id: UUID4) -> Order | None:
        for order in self.orders:
            if order.id == order_id:
                return order

        return None

    def add_round_to_order(self, order_id: UUID4, items: list[Item]) -> Order | None:
        for order in self.orders:
            if order.id == order_id:
                order.rounds.append(
                    Round(created=datetime.now(), items=items, id=uuid4())
                )
                return order

        return None

    def delete_round_from_order(self, order_id: UUID4, round_id: UUID4) -> Round | None:
        for i, order in enumerate(self.orders):
            if order.id != order_id:
                continue

            for j, round in enumerate(order.rounds):
                if round.id == round_id:
                    del self.orders[i].rounds[j]
                    return round

        return None

    def put_order(self, order: Order) -> Order:
        for i, repo_order in enumerate(self.orders):
            if repo_order.id == order.id:
                self.orders[i] = order
                return order

        order.created = datetime.now()
        order.id = uuid4()

        self.orders.append(order)
        return order

    def get_all_orders(self) -> list[Order]:
        return self.orders
