"""
Coinbase Brokerage Orderbook
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.coinbase import COINBASE_BROKERAGE_HTS_READ
from src.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_market_trades(client):
    """Gets tick data

    need to input start and end date
    max number of rows = 1000

    Args:
        client (_type_): coinbase brokerage client

    # 99  644921187    BTC-USD  70842.32       0.074  2024-05-21T08:42:50.792030Z   BUY          1716280970
    """
    data = client.get_market_trades("BTC-USD", {"start": 1714553344, "end": 1714556944})
    df_data = pd.DataFrame(data["trades"])
    df_data["datetime"] = pd.to_datetime(
        df_data["time"], format="%Y-%m-%dT%H:%M:%S.%fZ"
    )

    df_data["datetime"] = df_data["datetime"].astype("int64") // 10**9
    print(df_data)


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_HTS_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    get_market_trades(coinbase_client)
