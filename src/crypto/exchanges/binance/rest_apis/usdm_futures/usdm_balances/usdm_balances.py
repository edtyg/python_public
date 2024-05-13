"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from python.crypto.exchanges.binance.rest_apis.usdm_futures.usdm_account import (
    usdm_client_read,
)


def get_usdm_balances(client):
    """Gets Binance USD Margined account balances

    Args:
        client (_type_): binance usdm client
    """
    curr_time = dt.datetime.now()
    usdm_balances = client.get_account_balance()
    df_usdm_balances = pd.DataFrame(usdm_balances)

    df_usdm_balances["balance"] = df_usdm_balances["balance"].astype("float")
    df_usdm_balances = df_usdm_balances.loc[df_usdm_balances["balance"] > 0]

    df_usdm_balances["datetime"] = curr_time
    return df_usdm_balances


if __name__ == "__main__":

    df = get_usdm_balances(usdm_client_read)
    print(df)
