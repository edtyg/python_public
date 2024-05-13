"""
SPOT execution program
"""

import datetime as dt
from typing import Optional

import pandas as pd

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_spot_trade_history(client, spot_symbol: str, start_time: Optional[int] = None):
    """Gets spot trade history with time specified
    max of 1000 rows per api call
    easier to use start time

    Args:
        client (_type_): BinanceSpot client
        spot_symbol (str): "BTCUSDT
    """
    df_trades_final = pd.DataFrame()
    trade_status = False

    while trade_status is False:
        params = {
            "symbol": spot_symbol,
            "startTime": start_time,
            "limit": 1000,
        }
        trades = client.get_account_trade_list(params)
        df_trades = pd.DataFrame(trades)

        # gets df_orders_final latest time
        try:
            current_latest_time = df_trades_final.tail(1)["time"].values[0]
        except Exception as e:
            current_latest_time = 0
            print(e)

        # filters orders greater than latest time
        df_trades = df_trades.loc[df_trades["time"] > current_latest_time]
        if df_trades.empty is True:
            trade_status = True
        else:
            df_trades_final = pd.concat([df_trades_final, df_trades])
            latest_time = df_trades_final.tail(1)["time"].values[0]
            start_time = latest_time
            print(df_trades)

    df_trades_final["datetime"] = pd.to_datetime(df_trades_final["time"], unit="ms")
    return df_trades_final


if __name__ == "__main__":

    spot_symbol = "ETHUSDT"
    start_time = int(dt.datetime(2023, 1, 1, 12, 0, 0).timestamp() * 1000)

    orders = get_spot_trade_history(
        spot_client_read,
        spot_symbol,
        start_time,
    )
    print(orders)
