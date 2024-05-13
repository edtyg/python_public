"""
B2C2 Trade Records
"""

import pandas as pd

from local_credentials.api_work.crypto_brokers.b2c2 import B2C2_HTS_READ
from python.crypto.brokers.b2c2.rest.b2c2_client import B2C2Rest


def get_trade_records(client):
    """Gets Trade records

    Args:
        client (_type_): b2c2 spot client
    """
    trade_records = client.get_multiple_trades({"limit": 1000})
    df_trade_records = pd.DataFrame(trade_records)
    return df_trade_records


if __name__ == "__main__":
    account = B2C2_HTS_READ
    client = B2C2Rest(account["api_key"])

    df = get_trade_records(client)
    print(df)
