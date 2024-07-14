"""
pulling Kraken trades

"""

import pandas as pd

from src.crypto.exchanges.kraken.rest.kraken_client import Kraken


def get_ohlcv(client, ccy):
    data = client.get_ohlc_data({"pair": ccy, "interval": 60})["result"][ccy]
    column_names = ["time", "open", "high", "low", "close", "vwap", "volume", "count"]
    df_data = pd.DataFrame(data, columns=column_names)
    df_data["datetime"] = pd.to_datetime(df_data["time"], unit="s")
    df_data.set_index("datetime", inplace=True)
    return df_data


if __name__ == "__main__":
    client = Kraken()

    ticker = "BTC/USD"
    data = get_ohlcv(client, ticker)
    print(data)
