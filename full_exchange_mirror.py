import kalshi_python

from client.kalshi_client import AuthedApiInstance
from projects.market_making_scaffold.strategies.mirror_market_maker import (
    MirrorMarketMaker,
)

demo_config = kalshi_python.Configuration()
demo_config.api_key = {}
demo_config.host = "https://demo-api.kalshi.co/trade-api/v2"
demo_client = AuthedApiInstance(demo_config)

prod_config = kalshi_python.Configuration()
prod_config.api_key = {}
prod_client = AuthedApiInstance(
    username_key="prod_username",
    password_key="prod_password",
    config=prod_config,
)

market_maker = MirrorMarketMaker(True, demo_client, prod_client)
market_maker.safe_execute()
