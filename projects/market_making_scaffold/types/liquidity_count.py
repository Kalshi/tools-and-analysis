from dataclasses import dataclass
from projects.market_making_scaffold.types.side import Side


@dataclass
class LiquidityCount:
    side: Side
    count: int
    yes_price: int
