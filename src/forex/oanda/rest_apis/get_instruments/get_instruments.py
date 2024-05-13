"""
Get account ids and account details
"""

import pandas as pd

from keys.local_credentials.api_personal.forex_brokers.oanda import (
    OANDA_DEMO,
    OANDA_TRADE,
)
from src.forex.oanda.rest.oanda_client import Oanda


def get_account_instruments(client, account_id: str):
    """
    Gets tradable instruments for your account
    """

    instruments = client.get_account_instruments(account_id)
    df_instruments = pd.DataFrame(instruments["instruments"])
    return df_instruments


if __name__ == "__main__":
    account = OANDA_DEMO
    client = Oanda(account["api_key"])

    acc_id = "101-003-13096092-001"
    instru = get_account_instruments(client, acc_id)
    print(instru)
