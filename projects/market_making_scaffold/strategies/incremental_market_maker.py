from typing import Dict, List
from projects.market_making_scaffold.market_maker import MarketMaker
from kalshi_python.models import Order
from projects.market_making_scaffold.types import liquidity_count, side as book_side
from collections import defaultdict
from uuid import uuid4


class IncrementalMarketMaker(MarketMaker):
    """
    Performs minimal modifications to existing resting orders in order
    to achieve the desired book.
    """

    def update_book(
        self,
        market_ticker: str,
        resting_orders: List[Order],
        liquidity_counts: List[liquidity_count.LiquidityCount],
    ) -> None:
        for side in book_side.Side:
            self.update_book_side(
                market_ticker,
                side,
                [o for o in resting_orders if o.side == str(side)],
                [l for l in liquidity_counts if l.side == side],
            )

    def update_book_side(
        self,
        market_ticker: str,
        side: book_side.Side,
        resting_orders: List[Order],
        liquidity_counts: List[liquidity_count.LiquidityCount],
    ) -> None:
        resting_orders_by_yes_price: Dict[int, List[Order]] = defaultdict(list)
        desired_counts_by_yes_price: Dict[int, int] = defaultdict(0)

        for order in resting_orders:
            resting_orders_by_yes_price[order.yes_price].append(order)

        for liquidity_count in liquidity_counts:
            desired_counts_by_yes_price[
                liquidity_count.yes_price
            ] = liquidity_count.count

        for yes_price in range(1, 100):
            self.update_book_level(
                market_ticker,
                side,
                yes_price,
                resting_orders_by_yes_price[yes_price],
                desired_counts_by_yes_price[yes_price],
            )

    def update_book_level(
        self,
        market_ticker: str,
        side: book_side.Side,
        yes_price: int,
        resting_orders: List[Order],
        desired_count: int,
    ) -> None:
        # Note that this method gives no priority to orders by size or age.
        # Depending on desired behavior, it may make sense to prioritize
        # maintaing older or larger orders first.
        total_observed_order_count = 0

        for order in resting_orders:
            desired_order_size = min(
                order.remaining_count, desired_count - total_observed_order_count
            )
            if desired_order_size == 0:
                self.client.cancel_order(order_id=order.id)
            elif desired_order_size != order.remaining_count:
                self.client.modify_order(
                    order_id=order.id,
                    new_count=desired_order_size,
                )

            total_observed_order_count += desired_order_size

        if total_observed_order_count < desired_count:
            self.client.create_order(
                body={
                    "action": "buy",
                    # Note that the UUID is not currently used, but can be stored to
                    # avoid duplicate order placement.
                    "client_order_id": str(uuid4()),
                    "count": desired_count - total_observed_order_count,
                    "side": str(side),
                    "ticker": market_ticker,
                    "type": "limit",
                    "yes_price": yes_price,
                }
            )
