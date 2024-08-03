"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from keys.api_personal.crypto_exchanges.hashkey import HASHKEY_READ, HASHKEY_TRADE
from keys.api_work.crypto_exchanges.hashkey import HASHKEYEXCHANGE_HTS_MAIN_READ
from src.crypto.exchanges.hashkey_hk.rest.hashkey_spot_hk import HashkeySpot


def vip_info(client):
    vip = client.get_vip_info()
    return vip


def acc_info(client):
    account_info = client.get_account_info()
    return account_info


def acc_trades(client):
    trades = client.get_account_trade_list()
    return trades


def acc_type(client):
    account_type = client.get_query_account_type()
    return account_type


def fund_statement(client):
    statement = client.get_fund_statement(
        {
            "accountId": 1468177790721468160,
            "type": "trade",
            "startTime": 1720454400000,
            "endTime": 1720886400000,
        }
    )
    return statement


def get_opt_trade_records(client):
    opt_trades = client.get_opt_trades(
        {
            "accountType": "7",
            "pageNum": "1",
        }
    )
    return opt_trades


if __name__ == "__main__":
    account = HASHKEYEXCHANGE_HTS_MAIN_READ
    client = HashkeySpot(
        account["api_key"],
        account["api_secret"],
    )

    # vip_data = vip_info(client)
    # print(vip_data)

    # acc_info = acc_info(client)
    # print(acc_info)

    # trade = acc_trades(client)
    # print(trade)

    # account_type = acc_type(client)
    # print(account_type)

    # statement = fund_statement(client)
    # print(statement)

    # opt_trades = get_opt_trade_records(client)
    # print(opt_trades)

    traded_orders = client.get_all_traded_orders({"accountId": 1468013748774110722})
    print(traded_orders)
