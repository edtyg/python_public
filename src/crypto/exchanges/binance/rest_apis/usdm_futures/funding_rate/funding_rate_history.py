"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.usdm_futures.usdm_account import (
    usdm_client_read,
)


def get_funding_rate(client):
    """Gets Binance USD Margined funding rates

    Args:
        client (_type_): binance usdm client
    """
    rates = client.get_usdm_funding_rate_history(
        {
            "symbol": "ETHBTC",
            "limit": 1000,
        }
    )
    df_rates = pd.DataFrame(rates)
    df_rates["datetime"] = pd.to_datetime(df_rates["fundingTime"], unit="ms")
    df_rates.set_index("datetime", inplace=True)
    return df_rates


if __name__ == "__main__":

    df = get_funding_rate(usdm_client_read)
    print(df)
