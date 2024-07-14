"""
Get wallet transfer records
"""

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import (
    mca_ltp_client_read,
    spot_client_read,
)


def get_deposits(client):
    """

    Args:
        client (_type_): binance spot client
    """
    deposits = client.get_deposit_history()
    df_deposits = pd.DataFrame(deposits)
    df_deposits["datetime"] = pd.to_datetime(df_deposits["insertTime"], unit="ms")
    return df_deposits


if __name__ == "__main__":

    dep = get_deposits(mca_ltp_client_read)
    print(dep.columns)
