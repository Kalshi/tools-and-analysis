from typing import List
from projects.market_making_scaffold.market_maker import MarketMaker
from kalshi_python.models import Order
from projects.market_making_scaffold.types import desired_book, liquidity_count


class IncrementalMarketMaker(MarketMaker):
    def update_book(
        self,
        market_ticker: str,
        resting_orders: List[Order],
        liquidity_counts: List[liquidity_count.LiquidityCount],
    ) -> None:
        pass
