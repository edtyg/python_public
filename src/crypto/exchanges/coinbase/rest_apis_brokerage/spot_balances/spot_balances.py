"""
Coinbase Brokerage spot balances
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.coinbase import COINBASE_BROKERAGE_HTS_READ
from src.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_spot_balances(client):
    """Gets Spot balances

    Args:
        client (_type_): coinbase brokerage client
    """
    accounts = client.list_accounts()
    data = accounts["accounts"]
    df_spot_balances = pd.DataFrame(data)

    for i in df_spot_balances.index:
        df_spot_balances.loc[i, "avail_balance"] = df_spot_balances.loc[
            i, "available_balance"
        ]["value"]
        df_spot_balances.loc[i, "locked_balance"] = df_spot_balances.loc[i, "hold"][
            "value"
        ]
    df_spot_balances.drop(columns=["available_balance", "hold"], inplace=True)
    # df_spot_balances = df_spot_balances.loc[df_spot_balances["avail_balance"] != "0"]
    curr_time = dt.datetime.now()
    df_spot_balances["datetime"] = curr_time
    return df_spot_balances


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_HTS_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df = get_spot_balances(coinbase_client)
    print(df)
