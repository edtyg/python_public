"""
Coinbase Brokerage Top of order book data
"""

import pandas as pd

from keys.api_personal.crypto_exchanges.coinbase import COINBASE_BROKERAGE_READ
from src.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_bbo(client):
    """Gets Best bid and offer
    Args:
        client (_type_): coinbase brokerage spot client
    """

    bbo = client.get_best_bid_ask(
        {
            "product_ids": [
                "BTC-USDT",
                "ETH-USDT",
            ],
        }
    )
    df_bbo = pd.DataFrame(bbo["pricebooks"])
    return df_bbo


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df = get_bbo(coinbase_client)
    print(df)
