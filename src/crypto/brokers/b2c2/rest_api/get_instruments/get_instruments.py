"""
B2C2 tradable pairs and currencies
"""

import pandas as pd

from keys.api_work.crypto_brokers.b2c2 import B2C2_HTS_READ
from src.crypto.brokers.b2c2.rest.b2c2_client import B2C2Rest


def get_instruments(client):
    """
    Gets instruments that we can trade

    Args:
        client (_type_): b2c2 spot client
    """
    instruments = client.get_tradable_instruments()
    df_instruments = pd.DataFrame(instruments)
    return df_instruments


def get_currencies(client):
    """
    Gets Currencies that we can trade

    Args:
        client (_type_): b2c2 spot client
    """
    ccy = client.get_currencies()
    df_ccy = pd.DataFrame(ccy)
    df_ccy = df_ccy.T
    return df_ccy


if __name__ == "__main__":
    account = B2C2_HTS_READ
    client = B2C2Rest(account["api_key"])

    df_instruments = get_instruments(client)
    print(df_instruments)

    df_currencies = get_currencies(client)
    print(df_currencies)
