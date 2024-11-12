from fastapi import FastAPI, HTTPException

from pydantic import UUID4

from app.api.http import ItemRequest, OrdersResponse
from app.core.domain.models import Beer, Item, Order, Round, Stock
from app.core.services.services import Service
from app.repository.in_memory import InMemory


def start() -> FastAPI:
    app = FastAPI()

    # Inject
    service = Service(InMemory())

    @app.get("/stock")
    def all_stock() -> Stock:
        return service.get_all_stock()

    @app.get("/stock/{beer_id}")
    def get_beer(beer_id: UUID4) -> Beer | None:
        stock = service.get_stock_for_beer(beer_id)
        if stock is None:
            raise HTTPException(status_code=404, detail="beer not found in stock")

        return stock

    @app.put("/stock/{beer_id}")
    def put_beer(beer_id: UUID4, beer: Beer) -> Beer:
        beer.id = beer_id
        return service.put_stock(beer)

    @app.post("/stock/")
    def post_beer(beer: Beer) -> Beer:
        return service.put_stock(beer)

    @app.delete("/stock/{beer_id}")
    def delete_beer(beer_id: UUID4) -> Beer | None:
        beer = service.delete_stock(beer_id)
        if beer is None:
            raise HTTPException(status_code=404, detail="beer not found in stock")

        return beer

    @app.post("/orders/{order_id}/rounds")
    def post_round(order_id: UUID4, request: ItemRequest) -> Order:
        items: list[Item] = []

        for item in request.items:
            items.append(
                Item(
                    beer_id=item.beer_id,
                    quantity=item.quantity,
                    discount_flat=item.discount_flat,
                    discount_rate=item.discount_rate,
                )
            )

        result, err = service.add_round_to_order(order_id, items)

        if result is None:
            raise HTTPException(status_code=404, detail=err)

        return result

    # Technically an RPC call, uses post as it is not idempotent
    @app.post("/orders/{order_id}/pay")
    def close_tab(order_id: UUID4) -> Order:
        result, err = service.close_tab(order_id)
        if result is None:
            raise HTTPException(status_code=404, detail=err)

        return result

    @app.post("/orders/")
    def post_order() -> Order:
        return service.create_order()

    @app.get("/orders/{order_id}")
    def get_order(order_id: UUID4) -> Order | None:
        order = service.get_order(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="order not found")

        return order

    @app.get("/orders/")
    def get_all_orders() -> OrdersResponse:
        orders = service.get_all_orders()
        return OrdersResponse(orders=orders)

    @app.delete("/orders/{order_id}/rounds/{round_id}")
    def delete_round_from_order(order_id: UUID4, round_id: UUID4) -> Round | None:
        result = service.delete_round_from_order(order_id=order_id, round_id=round_id)
        if result is None:
            raise HTTPException(status_code=404, detail="round not found in order")
        return result

    return app