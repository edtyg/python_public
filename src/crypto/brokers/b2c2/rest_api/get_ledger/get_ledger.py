"""
B2C2 Ledger
"""

import pandas as pd

from keys.api_work.crypto_brokers.b2c2 import B2C2_HTS_READ
from src.crypto.brokers.b2c2.rest.b2c2_client import B2C2Rest


def get_ledger_df(client):
    """get ledger records"""

    ledger_data = client.get_ledger({"limit": 1000})
    df_ledger = pd.DataFrame(ledger_data)
    df_transfer = df_ledger.loc[df_ledger["type"] == "transfer"]
    df_transfer["amount"] = df_transfer["amount"].astype("float")
    for i in df_transfer.index:
        if df_transfer.loc[i, "amount"] < 0:
            df_transfer.loc[i, "transfer_type"] = "withdrawal"
        elif df_transfer.loc[i, "amount"] >= 0:
            df_transfer.loc[i, "transfer_type"] = "deposit"

    return df_transfer


if __name__ == "__main__":
    account = B2C2_HTS_READ
    client = B2C2Rest(account["api_key"])

    df_led = get_ledger_df(client)
    print(df_led)
