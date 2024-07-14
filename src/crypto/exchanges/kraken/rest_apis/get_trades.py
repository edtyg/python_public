"""
pulling Kraken trades

"""

import pandas as pd

from src.crypto.exchanges.kraken.rest.kraken_client import Kraken


def get_trades(client, ccy):
    data = client.get_recent_trades({"pair": ccy})["result"][ccy]
    column_names = [
        "price",
        "volume",
        "time",
        "direction",
        "order_type",
        "miscellaneous",
        "trade_id",
    ]
    df_data = pd.DataFrame(data, columns=column_names)
    df_data["direction"] = [
        "buy" if df_data.loc[i, "direction"] == "s" else "sell" for i in df_data.index
    ]
    df_data["order_type"] = [
        "limit" if df_data.loc[i, "order_type"] == "l" else "market"
        for i in df_data.index
    ]
    df_data["datetime"] = pd.to_datetime(df_data["time"], unit="s")
    df_data.set_index("datetime", inplace=True)

    return df_data


if __name__ == "__main__":
    client = Kraken()

    ticker = "WIF/USD"
    data = get_trades(client, ticker)
    print(data)
