"""
Coinbase Brokerage OHLCV
"""

import datetime as dt

import pandas as pd

from local_credentials.api_personal.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_candles(client):
    """
    Gets OHLCV

    Args:
        client (_type_): coinbase brokerage client

    ONE_MINUTE, ONE_HOUR, ONE_DAY
    """
    start_time = int(dt.datetime(2024, 3, 1, 12, 0, 0).timestamp())
    end_time = int(dt.datetime(2024, 3, 8, 12, 0, 0).timestamp())

    candles = client.get_product_candles(
        "BTC-USDT",
        {
            "start": start_time,
            "end": end_time,
            "granularity": "ONE_HOUR",
        },
    )
    df_candles = pd.DataFrame(candles["candles"])
    df_candles["datetime"] = pd.to_datetime(df_candles["start"], unit="s")
    return df_candles


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df = get_candles(coinbase_client)
    print(df)
