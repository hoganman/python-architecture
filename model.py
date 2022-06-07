""""""

import dataclasses
from typing import List, Dict, Optional, Set
from datetime import date

ID = str
Name = str
SKU = str
Quantity = int

STOCK_QUANTITY: Dict[SKU, Quantity] = {}


@dataclasses.dataclass(frozen=True)
class OrderLine(object):

    id: ID

    sku: SKU

    qty: Quantity


class Batch(object):

    def __init__(
            self,
            ref: ID,
            sku: SKU,
            qty: Quantity,
            eta: Optional[date] = None
    ):
        self.ref: ID = ref
        self.sku: SKU = sku
        self._purchased_quantity: Quantity = qty
        self.eta: Optional[date] = eta
        self._allocations: Set[OrderLine] = set()

    def allocate(self, order: OrderLine):
        self._allocations.add(order)

    def deallocate(self, order):
        if order in self._allocations:
            self._allocations.remove(order)

    @property
    def allocated_quantity(self):
        return sum(order.qty for order in self._allocations)

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, order: OrderLine) -> bool:
        return (
            order.sku == self.sku and (self.available_quantity - order.qty) >= 0
        )


@dataclasses.dataclass
class Product(object):

    sku: SKU

    name: Optional[str] = dataclasses.field(default=None)
