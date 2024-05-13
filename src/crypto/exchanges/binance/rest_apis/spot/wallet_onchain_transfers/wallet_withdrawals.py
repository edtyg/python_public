"""
Get wallet transfer records
"""

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_withdrawals(client):
    """

    Args:
        client (_type_): binance spot client
    """
    withdrawals = client.get_withdrawal_history()
    df_withdrawals = pd.DataFrame(withdrawals)
    return df_withdrawals


if __name__ == "__main__":

    withdraw = get_withdrawals(spot_client_read)
    print(withdraw)
