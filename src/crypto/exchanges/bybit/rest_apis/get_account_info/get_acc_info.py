"""
Bybit Account info - check if it's UTA
"""

import pandas as pd

from crypto.exchanges.bybit.rest_apis.accounts import spot_client_read


def acc_info(client):
    """
    Check on fees

    Args:
        client (_type_): bybit spot client
    """
    acc = client.get_account_info()
    return acc


def collateral_info(client):
    """
    Check on collateral settings

    Args:
        client (_type_): bybit spot client
    """
    acc_collateral = client.get_collateral_info()["result"]["list"]
    print(acc_collateral)
    df_data = pd.DataFrame(acc_collateral)
    return df_data


if __name__ == "__main__":

    acc = acc_info(spot_client_read)
    print(acc)

    coll = collateral_info(spot_client_read)
    print(coll)
