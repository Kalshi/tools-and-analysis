from typing import List
from kalshi_python.models import Order
from client.kalshi_client import AuthedApiInstance

from projects.market_making_scaffold.types import desired_book, liquidity_count
from abc import abstractmethod


class MarketMaker:
    def __init__(self, client: AuthedApiInstance):
        """
        Hook into websockets to keep track of resting orders.
        """
        self.client = client

    @abstractmethod
    def get_desired_book(self, market_ticker: str) -> desired_book.DesiredBook:
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
