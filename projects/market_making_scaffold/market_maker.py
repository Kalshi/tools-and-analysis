import traceback
from abc import abstractmethod
from time import sleep
from typing import List

from kalshi_python.models import GetOrdersResponse, Order

from client.kalshi_client import AuthedApiInstance
from projects.market_making_scaffold.types import liquidity_count


class MarketMaker:
    def __init__(self, client: AuthedApiInstance, is_advanced=False):
        # TODO: Setup a thread which maintains resting orders through
        # websockets.
        self.client = client
        self.is_advanced = is_advanced

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
        resting_orders: GetOrdersResponse = self.client.get_orders(
            ticker=market_ticker, status="resting"
        )

        # Necessary until the Python package is fixed
        for o in resting_orders.orders:
            del o["order_group_id"]

        self.update_book(
            market_ticker,
            [Order(**o) for o in resting_orders.orders],
            desired_book,
        )

    @abstractmethod
    def execute(self) -> None:
        """
        Run the market maker.
        """
        pass

    def safe_execute(self) -> None:
        """
        Run the market maker with protections in place, logging and restarting
        in the case of errors.
        """
        while True:
            try:
                self.execute()
            except Exception:
                print(traceback.format_exc())

                sleep(60)
                print("Restarting market maker...")
