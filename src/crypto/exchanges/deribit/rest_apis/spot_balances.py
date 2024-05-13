"""
Gets Spot Balances
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.deribit.rest_apis.deribit_account import deribit_read


def get_spot_balances(client):
    """
    Args:
        client (_type_): binance spot client
    """
    data = []
    ccy = ["BTC", "ETH", "USDC", "USDT"]
    for i in ccy:
        bal = client.get_account_summary({"currency": i})["result"]["available_funds"]
        data.append(bal)
    df_data = pd.DataFrame(data, index=ccy, columns=["spot_balance"])
    df_data["datetime"] = dt.datetime.now()
    return df_data


if __name__ == "__main__":
    df_balance = get_spot_balances(deribit_read)
    print(df_balance)
