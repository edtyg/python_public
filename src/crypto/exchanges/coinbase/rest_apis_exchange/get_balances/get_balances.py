"""
Coinbase Exchange Balances
"""

import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_exchanges.coinbase import (
    COINBASE_EXCHANGE_HTS_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_exchange_client import (
    CoinbaseExchange,
)


def get_balances(client):
    """Gets balances

    Args:
        client (_type_): coinbase exchange client
    """
    account_balance = client.get_all_accounts()
    df_account_balance = pd.DataFrame(account_balance)
    df_account_balance["balance"] = df_account_balance["balance"].astype("float")
    # df_account_balance = df_account_balance.loc[df_account_balance["balance"] != 0]
    df_account_balance["datetime"] = dt.datetime.now()
    return df_account_balance


if __name__ == "__main__":
    account = COINBASE_EXCHANGE_HTS_READ
    client = CoinbaseExchange(
        account["api_key"],
        account["api_secret"],
        account["passphrase"],
    )

    accounts = get_balances(client)
    print(
        accounts.loc[accounts["currency"].isin(["BTC", "ETH", "USDT", "USDC", "USD"])]
    )
