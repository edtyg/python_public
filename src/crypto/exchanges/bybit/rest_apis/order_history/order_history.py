"""
Bybit Spot Account balances
"""

import pandas as pd

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_TRADE
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


def get_order_history(client):
    """
    Check on historical orders of up to 2 years

    Args:
        client (_type_): bybit spot client
    """
    order_history = client.get_order_history(
        {
            "category": "spot",
            "symbol": "ETHUSDT",
        }
    )
    data = order_history["result"]["list"]
    df_order_history = pd.DataFrame(data)
    return df_order_history


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_TRADE
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    order_hist = get_order_history(client)
    print(order_hist)
