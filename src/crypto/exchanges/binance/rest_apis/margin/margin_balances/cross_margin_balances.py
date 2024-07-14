"""
Cross Margin Balances
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.margin.margin_account import (
    xmargin_client_read,
)


def get_cross_margin_balances(client):
    """
    Args:
        client (_type_): binance margin client
    """
    curr_time = dt.datetime.now()
    cross_margin_balance = client.get_cross_margin_details()
    print(cross_margin_balance)
    df_balance = pd.DataFrame(cross_margin_balance["userAssets"])
    df_balance["datetime"] = curr_time
    df_balance["netAsset"] = df_balance["netAsset"].astype("float")
    df_balance = df_balance.loc[df_balance["netAsset"] > 0]
    return df_balance


if __name__ == "__main__":

    df = get_cross_margin_balances(xmargin_client_read)
    print(df)
