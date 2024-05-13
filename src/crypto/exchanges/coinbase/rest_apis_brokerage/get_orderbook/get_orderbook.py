"""
Coinbase Brokerage Orderbook
"""

import pandas as pd

from local_credentials.api_personal.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_orderbook(client):
    """Gets Best bid and offer
    Args:
        client (_type_): coinbase brokerage client


    ONE_MINUTE, ONE_HOUR, ONE_DAY
    """
    orderbook = client.get_product_book({"product_id": "BTC-USDT", "limit": 10})
    df_orderbook_bids = pd.DataFrame(orderbook["pricebook"]["bids"])
    df_orderbook_asks = pd.DataFrame(orderbook["pricebook"]["asks"])

    df_orderbook_bids["type"] = "bids"
    df_orderbook_asks["type"] = "asks"

    return df_orderbook_bids, df_orderbook_asks


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df_bids, df_asks = get_orderbook(coinbase_client)
    print(df_bids)
    print(df_asks)
