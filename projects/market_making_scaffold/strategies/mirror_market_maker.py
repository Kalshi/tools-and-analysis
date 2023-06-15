import traceback
from time import sleep
from typing import List

from kalshi_python.models import GetMarketsResponse, OrderBook

from client.kalshi_client import AuthedApiInstance
from projects.market_making_scaffold.strategies.incremental_market_maker import (
    IncrementalMarketMaker,
)
from projects.market_making_scaffold.types.liquidity_count import LiquidityCount
from projects.market_making_scaffold.types.side import Side


class MirrorMarketMaker(IncrementalMarketMaker):
    def __init__(
        self,
        is_advanced: bool,
        client: AuthedApiInstance,
        mirror_client: AuthedApiInstance,
    ):
        self.mirror_client = mirror_client
        super().__init__(client, is_advanced)

    def get_desired_book(self, market_ticker: str) -> List[LiquidityCount]:
        orderbook: OrderBook = self.mirror_client.get_market_orderbook(
            ticker=market_ticker
        ).orderbook

        yes_liquidity = [
            LiquidityCount(Side.YES, entry[1], entry[0]) for entry in orderbook.yes
        ]
        no_liquidity = [
            LiquidityCount(Side.NO, entry[1], 100 - entry[0]) for entry in orderbook.no
        ]

        self.client.get_market_orderbook(ticker=market_ticker)

        return yes_liquidity + no_liquidity

    def execute(self) -> None:
        markets: GetMarketsResponse = self.client.get_markets(status="open")

        while len(markets.markets) > 0:
            for market in markets.markets:
                print(market.ticker)

                try:
                    self.refresh_market(market.ticker)
                except Exception:
                    print("Failed to refresh market:", market.ticker)
                    traceback.print_exc()

            markets = self.client.get_markets(status="open", cursor=markets.cursor)

            sleep(0.2)
