from datetime import date, timedelta
import pytest

from model import (
    Batch, OrderLine, Product
)

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

small_table = Product(sku="SMALL-TABLE")
blue_cushion = Product(sku="BLUE-CUSHION")


def test_allocating_to_a_batch_reduces_the_available_quantity():
    start_batch_quantity, order_quantity = 20, 2
    batch = Batch("batch-SMALL-TABLE", small_table.sku, start_batch_quantity)
    order_line = OrderLine("order-SMALL-TABLE", small_table.sku, order_quantity)

    batch.allocate(order_line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    start_batch_quantity, order_quantity = 2, 1
    batch = Batch("batch-BLUE-CUSHION", blue_cushion.sku, start_batch_quantity)
    order_line = OrderLine("order-BLUE-CUSHION", blue_cushion.sku, order_quantity)
    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_available_smaller_than_required():
    start_batch_quantity, order_quantity = 1, 2
    batch = Batch("batch-BLUE-CUSHION", blue_cushion.sku, start_batch_quantity)
    order_line = OrderLine("order-BLUE-CUSHION", blue_cushion.sku, order_quantity)
    assert not batch.can_allocate(order_line)


def test_can_allocate_if_available_equal_to_required():
    start_batch_quantity, order_quantity = 20, 20
    batch = Batch("batch-BLUE-CUSHION", blue_cushion.sku, start_batch_quantity)
    order_line = OrderLine("order-BLUE-CUSHION", blue_cushion.sku, order_quantity)
    assert batch.can_allocate(order_line)


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")
