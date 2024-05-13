"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from local_credentials.api_personal.crypto_exchanges.hashkey import (
    HASHKEY_READ,
    HASHKEY_TRADE,
)
from python.crypto.exchanges.hashkey.rest.hashkey_hk.hashkey_client_hk import (
    HashkeyExchange,
)


def get_account_type(client):
    """Gets Account Type

    Args:
        client (_type_): hashkey spot client
    """
    accounts = client.query_account_type()
    df_accounts = pd.DataFrame(accounts)
    return df_accounts


def get_trading_balances(client):
    """Gets balances for trading account

    Args:
        client (_type_): hashkey spot client

    accountId:
    1100362 -> Main trading Account
    1200362 -> Custody Account
    1300362 -> Fiat Account
    """
    status = False
    while status is False:
        try:
            trading_balances = client.get_account_info(params={"accountId": 1100362})
            df_trading_balances = pd.DataFrame(trading_balances["balances"])
            if df_trading_balances.empty:
                status = True
                continue
            df_trading_balances["account"] = "trading_account"
            status = True
            continue
        except Exception as e:
            print(e)

    return df_trading_balances


def get_custody_balances(client):
    """Gets balances for custody account

    Args:
        client (_type_): hashkey spot client

    accountId:
    1100362 -> Main trading Account
    1200362 -> Custody Account
    1300362 -> Fiat Account
    """
    status = False
    while status is False:
        try:
            custody_balances = client.get_account_info(params={"accountId": 1200362})
            df_custody_balances = pd.DataFrame(custody_balances["balances"])
            if df_custody_balances.empty:
                status = True
                continue
            df_custody_balances["account"] = "custody_account"
            status = True
            continue
        except Exception as e:
            print(e)

    return df_custody_balances


def get_fiat_balances(client):
    """Gets balances for fiat account

    Args:
        client (_type_): hashkey spot client

    accountId:
    1100362 -> Main trading Account
    1200362 -> Custody Account
    1300362 -> Fiat Account
    """
    status = False
    while status is False:
        try:
            fiat_balances = client.get_account_info(params={"accountId": 1300362})
            df_fiat_balances = pd.DataFrame(fiat_balances["balances"])
            if df_fiat_balances.empty:
                status = True
                continue
            df_fiat_balances["account"] = "fiat_account"
            status = True
            continue
        except Exception as e:
            print(e)

    return df_fiat_balances


if __name__ == "__main__":
    account = HASHKEY_READ
    client = HashkeyExchange(
        account["api_key"],
        account["api_secret"],
    )

    # df_acc_types = get_account_type(client)
    # print(df_acc_types)

    df_trading_balances = get_trading_balances(client)
    print(df_trading_balances)

    df_custody_balances = get_custody_balances(client)
    print(df_custody_balances)

    df_fiat_balances = get_fiat_balances(client)
    print(df_fiat_balances)
