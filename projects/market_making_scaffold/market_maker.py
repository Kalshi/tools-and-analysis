from typing import Dict, List
from kalshi_python.models import Order
from client.kalshi_client import AuthedApiInstance

from collections import defaultdict
from projects.market_making_scaffold.types import liquidity_count
from abc import abstractmethod


class MarketMaker:
    def __init__(self, client: AuthedApiInstance):
        """
        Hook into websockets to keep track of resting orders.
        """
        self.client = client
        self.resting_orders_by_market: Dict[str, List[Order]] = defaultdict(list)

        # TODO: Setup a thread which maintains resting orders through websockets.
        client.get_orders()

    @abstractmethod
    def get_desired_book(
        self, market_ticker: str
    ) -> List[liquidity_count.LiquidityCount]:
        """
        Given a market ticker, return a desired book.
        """
        pass

    @abstractmethod
    def update_book(
        self,
        market_ticker: str,
        resting_orders: List[Order],
        liquidity_counts: List[liquidity_count.LiquidityCount],
    ) -> None:
        pass

    def refresh_market(self, market_ticker: str) -> None:
        """
        Given a market ticker, refresh the market.
        """
        desired_book = self.get_desired_book(market_ticker)
        resting_orders = self.client.get_orders(ticker=market_ticker, status="resting")

        self.update_book(
            market_ticker,
            resting_orders,
            desired_book,
        )
