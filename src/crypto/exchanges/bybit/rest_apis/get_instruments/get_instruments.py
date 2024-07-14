"""
Bybit Instruments
"""

import pandas as pd

from src.crypto.exchanges.bybit.rest_apis.accounts import spot_client_read


def get_instruments(client):
    """Gets bybit tradable instruments
    need to specify instrument category

    Args:
        client (_type_): bybit client
    """

    inst = client.get_instruments_info({"category": "spot", "symbol": "BTCUSDT"})
    data = inst["result"]["list"]
    return data


if __name__ == "__main__":
    instruments = get_instruments(spot_client_read)
    print(instruments)
