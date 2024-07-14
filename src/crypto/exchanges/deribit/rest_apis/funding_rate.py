"""
Gets Spot Balances
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.deribit.rest_apis.deribit_account import deribit_read


def get_funding_history(client):
    """
    Args:
        client (_type_): binance spot client
    """
    data = client.get_funding_rate_history(
        {
            "instrument_name": "BTC-PERPETUAL",
            "start_timestamp": 1704081600000,
            "end_timestamp": 1719363661000,
        }
    )
    df_data = pd.DataFrame(data["result"])
    df_data["datetime"] = pd.to_datetime(df_data["timestamp"], unit="ms")
    return df_data


if __name__ == "__main__":
    funding = get_funding_history(deribit_read)
    print(funding)
