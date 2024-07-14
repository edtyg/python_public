"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.okx import OKX_MCA_LTP1_READ
from src.crypto.exchanges.okx.rest.okx_client import Okx


def get_trading_account_balances(client):
    """Gets funding account balances

    Args:
        client (_type_): okx spot client
    """
    curr_time = dt.datetime.now()
    trading_balances = client.get_balance_trading()
    data = trading_balances["data"][0]["details"]
    df_trading_balances = pd.DataFrame(data)

    df_trading_balances["datetime"] = curr_time
    return df_trading_balances


if __name__ == "__main__":
    account = OKX_MCA_LTP1_READ
    okx_client = Okx(
        apikey=account["api_key"],
        apisecret=account["api_secret"],
        passphrase=account["passphrase"],
    )

    trading_balance = get_trading_account_balances(okx_client)
    print(trading_balance)
