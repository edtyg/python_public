"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.coinm_futures.coinm_account import (
    coinm_client_read,
)


def get_funding_rate(client):
    """Gets Binance USD Margined funding rates

    Args:
        client (_type_): binance usdm client
    """
    rates = client.get_coinm_funding_rate(
        {
            "symbol": "ETHUSD_PERP",
            "limit": 1000,
        }
    )
    # print(rates)
    df_rates = pd.DataFrame(rates)
    df_rates["datetime"] = pd.to_datetime(df_rates["fundingTime"], unit="ms")
    df_rates.set_index("datetime", inplace=True)
    return df_rates


if __name__ == "__main__":
    df = get_funding_rate(coinm_client_read)
    print(df)
