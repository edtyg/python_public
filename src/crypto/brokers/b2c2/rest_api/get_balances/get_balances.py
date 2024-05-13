"""
B2C2 Balances
"""

import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_brokers.b2c2 import B2C2_HTS_MAIN
from python.crypto.brokers.b2c2.rest.b2c2_client import B2C2Rest


def get_spot_balances(client):
    """Gets B2C2 balances

    Args:
        client (_type_): b2c2 client
    """
    symbol_mapping = {
        "USC": "USDC",
        "UST": "USDT",
    }

    curr_time = dt.datetime.now()
    spot_balances = client.get_balances()

    df_spot = pd.DataFrame(list(spot_balances.items()), columns=["coin", "amount"])
    for i in df_spot.index:
        symbol = df_spot.loc[i, "coin"]
        if symbol in symbol_mapping:
            df_spot.loc[i, "coin"] = symbol_mapping[symbol]

    # Convert 'Value' column to numeric type
    df_spot["amount"] = pd.to_numeric(df_spot["amount"])
    df_spot = df_spot.loc[df_spot["amount"] != 0]
    df_spot["datetime"] = curr_time
    return df_spot


if __name__ == "__main__":
    account = B2C2_HTS_MAIN
    client = B2C2Rest(account["api_key"])

    df = get_spot_balances(client)
    print(df)
