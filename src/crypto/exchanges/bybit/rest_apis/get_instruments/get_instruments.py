"""
Bybit Spot Account balances
"""

import pandas as pd

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_READ
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


def get_instruments(client):
    """Gets bybit tradable instruments
    need to specify instrument category

    Args:
        client (_type_): bybit client
    """

    inst = client.get_instruments_info({"category": "spot", "symbol": "BTCUSDT"})
    data = inst["result"]["list"]
    df_data = pd.DataFrame(data)
    return inst


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_READ
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    instruments = get_instruments(client)
    print(instruments)
