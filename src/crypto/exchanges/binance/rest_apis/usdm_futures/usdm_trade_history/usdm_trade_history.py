"""
SPOT execution program
"""

import datetime as dt
from typing import Optional

import pandas as pd

from python.crypto.exchanges.binance.rest_apis.usdm_futures.usdm_account import (
    usdm_client_read,
)


def get_usdm_trade_history(
    client,
    usdm_symbol: str,
    start_time: Optional[int] = None,
):
    """Gets usdm trade history with time specified
    max of 1000 rows per api call
    easier to use start time

    Args:
        client (_type_): BinanceUsdm client
        spot_symbol (str): "BTCUSDT
    """
    df_orders_final = pd.DataFrame()
    order_status = False

    while order_status is False:
        params = {
            "symbol": usdm_symbol,
            "startTime": start_time,
            "limit": 1000,
        }
        orders = client.get_account_trade_list(params)
        df_orders = pd.DataFrame(orders)

        # gets df_orders_final latest time
        try:
            current_latest_time = df_orders_final.tail(1)["time"].values[0]
        except Exception as e:
            current_latest_time = 0
            print(e)

        # filters orders greater than latest time
        df_orders = df_orders.loc[df_orders["time"] > current_latest_time]
        if df_orders.empty is True:
            order_status = True
        else:
            df_orders_final = pd.concat([df_orders_final, df_orders])
            latest_time = df_orders_final.tail(1)["time"].values[0]
            start_time = latest_time
            print(df_orders)

    df_orders_final["datetime"] = pd.to_datetime(df_orders_final["time"], unit="ms")
    print(df_orders_final)
    return df_orders_final


if __name__ == "__main__":

    usdm_symbol = "BTCUSDT"

    # only within 3 months
    start_time = int(dt.datetime(2023, 10, 15, 12, 0, 0).timestamp() * 1000)

    orders = get_usdm_trade_history(
        usdm_client_read,
        usdm_symbol,
        start_time,
    )
