"""
GETS trading fees
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_fees(client):
    """

    Args:
        client (_type_): binance spot client
    """
    fee = client.get_trade_fee()
    df_fee = pd.DataFrame(fee)
    return df_fee


if __name__ == "__main__":

    fees = get_fees(spot_client_read)
    print(fees)
