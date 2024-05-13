# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:31:24 2024

@author: Edgar Tan
"""

import datetime as dt
import math

import pandas as pd
import requests


def pull_spot_klines(ticker: str, start_time: int, end_time: int):
    """pull spot klines -
    to include start and end time

    Args:
        ticker (str): "BTCUSD_210924"
        start_time (int): 1723780800000
        end_time (int): 1723780800000
    """
    url = "https://api.binance.com/api/v3/klines"
    df_col_name = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "placeholder",
    ]
    # 1000 rows * 60 seconds * 1000 to convert to milliseconds
    max_interval = 1000 * 60 * 1000

    if end_time < start_time:
        print("select a different timeframe - end_time has to be > start_time")
        return

    elif end_time < start_time + max_interval:
        print("endtime requires only 1 loop")

        params = {
            "symbol": ticker,
            "interval": "1m",
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000,
        }
        resp = requests.get(
            url=url,
            params=params,
            timeout=5,
        )
        data = resp.json()
        df = pd.DataFrame(data, columns=df_col_name)
        df["open_datetime_utc"] = pd.to_datetime(df["open_time"], unit="ms")
        return df

    else:
        print("requires more than 1 loop")
        df_new = pd.DataFrame()
        i = 1
        number_of_loops = math.ceil((end_time - start_time) / max_interval)
        print(number_of_loops)
        while i <= number_of_loops:
            print(i)
            params = {
                "symbol": ticker,
                "interval": "1m",
                "startTime": start_time,
                "endTime": start_time + max_interval,
                "limit": 1000,
            }
            resp = requests.get(
                url=url,
                params=params,
                timeout=3,
            )
            data = resp.json()
            df = pd.DataFrame(data, columns=df_col_name)
            df["open_datetime_utc"] = pd.to_datetime(df["open_time"], unit="ms")
            df_new = pd.concat([df_new, df])
            start_time = start_time + max_interval
            i += 1
        return df_new.drop_duplicates()


if __name__ == "__main__":

    symbol = "BTCUSDT"
    start_time = int(dt.datetime(2024, 1, 20, 0, 0, 0).timestamp() * 1000)  # start time
    end_time = int(dt.datetime(2024, 1, 28, 12, 0, 0).timestamp() * 1000)  # end time

    data = pull_spot_klines(symbol, start_time, end_time)
    print(data)
