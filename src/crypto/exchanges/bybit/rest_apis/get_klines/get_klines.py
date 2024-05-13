"""
Bybit Spot Account balances
"""

import pandas as pd

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_READ
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


def get_kline(client):
    """Gets bybit klines
    need to specify instrument category

    Args:
        client (_type_): bybit client
    """

    symbol_kline = client.get_kline(
        {
            "category": "spot",
            "symbol": "BTCUSDT",
            "interval": "60",
        }
    )
    data = symbol_kline["result"]["list"]
    columns = ["startTime", "open", "high", "low", "close", "volume", "turnover"]
    df_data = pd.DataFrame(data, columns=columns)
    df_data["datetime"] = pd.to_datetime(
        df_data["startTime"].astype("float"), unit="ms"
    )
    return df_data


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_READ
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    klines = get_kline(client)
    print(klines)
