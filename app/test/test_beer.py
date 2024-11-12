from app.core.domain.models import Beer, Item
from app.core.services.services import Service
from app.repository.in_memory import InMemory


def test_add_beer_to_stock() -> None:
    # Setup
    service = Service(InMemory())
    beer = service.put_stock(Beer(name="TestBeer1", price=234, quantity=2))

    stock = service.get_stock_for_beer(beer.id)

    # Assert
    if stock is None:
        assert False

    assert stock.price == 234


def test_add_round_to_order() -> None:
    # Setup
    service = Service(InMemory())
    beer1 = service.put_stock(Beer(name="TestBeer1", price=100, quantity=6))
    beer2 = service.put_stock(Beer(name="TestBeer2", price=200, quantity=5))
    beer3 = service.put_stock(Beer(name="TestBeer3", price=300, quantity=2))

    order = service.create_order()

    items = [
        Item(beer_id=beer1.id, quantity=2),
        Item(beer_id=beer2.id, quantity=2),
        Item(beer_id=beer3.id, quantity=1),
    ]

    result, _ = service.add_round_to_order(order.id, items)

    items2 = [
        Item(beer_id=beer2.id, quantity=2),
        Item(beer_id=beer3.id, quantity=1),
    ]

    result, _ = service.add_round_to_order(order.id, items2)

    # Assert
    if result is None:
        assert False

    assert len(order.rounds) == 2
    assert result.rounds[0].items[0].beer_id == beer1.id
    assert result.rounds[0].items[1].beer_id == beer2.id
    assert result.rounds[0].items[2].beer_id == beer3.id

    # Check if stock has gone down
    stock_beer_1 = service.get_stock_for_beer(beer1.id)
    stock_beer_2 = service.get_stock_for_beer(beer2.id)
    stock_beer_3 = service.get_stock_for_beer(beer3.id)

    if stock_beer_1 is None or stock_beer_2 is None or stock_beer_3 is None:
        assert False

    assert stock_beer_1.quantity == 4
    assert stock_beer_2.quantity == 1
    assert stock_beer_3.quantity == 0


def test_reject_round_due_to_no_stock() -> None:
    # Setup
    service = Service(InMemory())
    beer1 = service.put_stock(Beer(name="TestBeer1", price=100, quantity=2))
    beer2 = service.put_stock(Beer(name="TestBeer2", price=200, quantity=5))
    beer3 = service.put_stock(Beer(name="TestBeer3", price=300, quantity=2))

    order = service.create_order()

    items = [
        Item(beer_id=beer1.id, quantity=2),
        Item(beer_id=beer2.id, quantity=6),
        Item(beer_id=beer3.id, quantity=2),
    ]

    result, err = service.add_round_to_order(order.id, items)

    # Assert
    assert result is None
    assert err == "not enough beer in stock: 5 TestBeer2(s) left, 6 requested"


def test_close_tab() -> None:
    # Setup
    service = Service(InMemory())
    beer1 = service.put_stock(Beer(name="TestBeer1", price=100, quantity=2))
    beer2 = service.put_stock(Beer(name="TestBeer2", price=200, quantity=5))
    beer3 = service.put_stock(Beer(name="TestBeer3", price=300, quantity=2))

    order = service.create_order()

    items = [
        Item(beer_id=beer1.id, quantity=2),
        Item(beer_id=beer2.id, quantity=1),
        Item(beer_id=beer3.id, quantity=1),
    ]

    service.add_round_to_order(order.id, items)

    items = [
        Item(beer_id=beer2.id, quantity=1, discount_flat=50),
        Item(beer_id=beer3.id, quantity=1, discount_rate=0.10),
    ]

    service.add_round_to_order(order.id, items)

    tab, _ = service.close_tab(order.id)

    if tab is None:
        assert False

    # 300 * 0.1 = 170
    # 200 - 50 = 150
    # 100 * 2 + 200 + 300 = 700
    # discounts = 30 + 50 = 80
    # taxes = 1120 * 0.18 = 201.6
    # total = 1200 - 80 + 201.6 = 1321.6

    # Assert
    assert tab.id == order.id
    assert tab.paid is True
    assert tab.sub_total == 1200.0
    assert tab.taxes == 201.6
    assert tab.total == 1321.6
    assert tab.discounts == 80.0

    assert len(tab.rounds) == 2
