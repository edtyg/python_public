"""
Bybit Spot Account balances
"""

import pandas as pd

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_TRADE
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


def get_internal_trans(client):
    """
    Check on internal transf within same account

    Args:
        client (_type_): bybit spot client
    """
    transf_hist = client.get_internal_transfer_records()
    data = transf_hist["result"]["list"]
    df_data = pd.DataFrame(data)
    return df_data


def get_univ_trans(client):
    """
    Check on universal transf within same accoun
    Args:
        client (_type_): bybit spot client
    """
    transf_hist = client.get_universal_transfer_records()
    data = transf_hist["result"]["list"]
    df_data = pd.DataFrame(data)
    df_data["datetime"] = pd.to_datetime(df_data["timestamp"], unit="ms")

    return df_data


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_TRADE
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    # int_transf = get_internal_trans(client)
    # print(int_transf)

    univ_transf = get_univ_trans(client)
    print(univ_transf)
