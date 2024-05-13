"""
Gets Spot Balances
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_spot_balances(client):
    """
    Args:
        client (_type_): binance spot client
    """

    curr_time = dt.datetime.now()
    spot_balances = client.post_user_asset()
    df_spot_balances = pd.DataFrame(spot_balances)
    df_spot_balances["datetime"] = curr_time
    return df_spot_balances


if __name__ == "__main__":

    df_balance = get_spot_balances(spot_client_read)
    print(df_balance)
