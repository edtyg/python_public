"""
Coinbase Brokerage - place orders
"""

import datetime as dt

from local_credentials.api_personal.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_TRADE,
)
from python.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def place_order(client):
    """
    Places order on brokerage account
    Client order id must be unique

    Args:
        client (_type_): coinbase brokerage client

    """
    curr_time = int(dt.datetime.now().timestamp())

    order = client.create_order(
        params={
            "client_order_id": f"test_{curr_time}",
            "product_id": "PAX-USDC",
            "side": "BUY",
            "order_configuration": {
                "limit_limit_gtc": {
                    "base_size": "10",
                    "limit_price": "0.9",
                }
            },
        }
    )
    print(order)
    return order


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_TRADE
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    order1 = place_order(coinbase_client)
