"""
Isolated Margin Balances
"""

import datetime as dt

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.margin.margin_account import (
    margin_client_read,
)


def get_isolated_margin_balances(client):
    """Gets cross margin account balances

    Args:
        client (_type_): binance cross margin client
    """
    df_final = pd.DataFrame()
    curr_time = dt.datetime.now()
    iso_margin_balance = client.get_isolated_margin_details()
    assets = iso_margin_balance["assets"]

    for i in assets:
        symbol = i["symbol"]
        base_asset = i["baseAsset"]["asset"]
        base_asset_amt = i["baseAsset"]["netAsset"]
        quote_asset = i["quoteAsset"]["asset"]
        quote_asset_amt = i["quoteAsset"]["netAsset"]
        asset_dict = {
            "isolated_margin_symbol": symbol,
            "base_asset": base_asset,
            "base_asset_amt": base_asset_amt,
            "quote_asset": quote_asset,
            "quote_asset_amt": quote_asset_amt,
        }
        df_asset = pd.DataFrame(asset_dict, index=[0])
        df_final = pd.concat([df_final, df_asset])

    df_final["datetime"] = curr_time
    return df_final


if __name__ == "__main__":
    df = get_isolated_margin_balances(margin_client_read)
    print(df)
