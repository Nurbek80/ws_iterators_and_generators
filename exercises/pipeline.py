from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass(frozen=True)
class Order:
    id: int
    order_id: str
    customer_name: str
    customer_email: str
    product: str
    category: str
    amount: int
    unit_price: float
    order_date: str
    country: str
    status: str
    line_error: bool = False


class Orders:
    """Reusable iterable that produces a fresh iterator for every iteration."""

    def __init__(self, lines: Iterator[str]) -> None:
        self._iter_lines = list(lines)

    def __iter__(self) -> Iterator[Order]:
        # TODO: return a Orders iterator
        return OrdersIterator(iter(self._iter_lines))


class OrdersIterator:
    """Stateful iterator over CSV-like lines."""

    def __init__(self, lines: Iterator[str]) -> None:
        # TODO: save the lines and initialize the cursor
        self.lines = list(lines)
        self.cursor = 0
    
    def __iter__(self) -> OrdersIterator:
        # TODO: an iterator must return itself
        return self
        
    @staticmethod
    def _line_parser(line: str, index: int) -> Order:
        try:
            parts = line.strip().split(',')
            return Order(
                id=index,
                order_id=parts[0],
                customer_name=parts[1],
                customer_email=parts[2],
                product=parts[3],
                category=parts[4],
                amount=int(parts[5]),
                unit_price=float(parts[6]),
                order_date=parts[7],
                country=parts[8],
                status=parts[9],
                line_error=False
            )
        except Exception as e:
            print(f"Error parsing line {index}: {e}")

            return Order(
                id=index, order_id="", customer_name="", customer_email="",
                product="", category="", amount=0, unit_price=0.0,
                order_date="", country="", status="", line_error=True
            )

    def __next__(self) -> Order:
        # TODO: Return the next order.
        if self.cursor >= len(self.lines):
            raise StopIteration
        
        current_line = self.lines[self.cursor]
        order = self._line_parser(current_line, self.cursor)
        
        self.cursor += 1
        return order
    

def paid_sales(orders: Orders) -> Iterator[Order]:
    """Yield only paid orders."""
    # TODO: implement as a generator
    for order in orders:
        if order.status.strip().lower() == "paid":
            yield order


def above_threshold(
    orders: Iterable[Order],
    threshold: int,
) -> Iterator[Order]:
    """Yield only orders with an <price * amount> greater than or equal to threshold."""
    # TODO: implement as a generator
    for order in orders:
        if (order.amount * order.unit_price) >= threshold:
            yield order


def report_all_sales(
    orders: Orders,
    threshold: int,
) -> tuple[int, float]:
    """Report total amount and total revenue for paid orders above threshold."""
    # FIX: this function has a bug, the total_order_count is always 0
    selected = above_threshold(paid_sales(orders), threshold=threshold)
    
    selected_list = list(selected)
    total_sum = sum(order.amount * order.unit_price for order in selected_list)
    total_order_count = len(selected_list)
    
    return (total_order_count, total_sum)