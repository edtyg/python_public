"""
OKX V5 API
https://www.okx.com/docs-v5/en/#overview
"""

import datetime as dt
import time

import pandas as pd

from local_credentials.api_work.crypto_exchanges.okx import OKX_MCA_MAIN_READ
from python.crypto.exchanges.okx.rest.okx_client import Okx


def get_candles(client):
    start_ts = int(dt.datetime(2023, 8, 17, 0, 0, 0).timestamp() * 1000)  # utc time
    end_ts = int(dt.datetime(2023, 8, 23, 0, 0, 0).timestamp() * 1000)
    print(f"start_ts = {start_ts}")
    print(f"end_ts = {end_ts}")

    df_final = pd.DataFrame()  # empty dataframe

    end_time = 0
    while end_time < end_ts:
        try:
            data = client.get_candlesticks_history(
                {
                    "instId": "BTC-USDT",
                    "bar": "1m",
                    "limit": 100,  # default = 100, max = 100
                    "after": start_ts,
                }
            )
            column_name = [
                "ts",
                "open",
                "high",
                "low",
                "close",
                "volume",  # Trading volume, with a unit of contract.
                "volume_ccy",  # Trading volume, with a unit of currency.
                "volume_ccy_quote",  # Trading volume, the value is the quantity in quote currency
                "confirm",  # state of ticker -> 0 means uncompleted
            ]

            data_candles = data["data"]
            df_data_candles = pd.DataFrame(data_candles, columns=column_name)
            df_data_candles["datetime"] = pd.to_datetime(
                df_data_candles["ts"].astype("float"), unit="ms"
            )

            df_final = pd.concat([df_final, df_data_candles])
            df_final.sort_values(by=["datetime"], ascending=False, inplace=True)
            print(df_data_candles)
            df_final.reset_index(inplace=True, drop=True)

            start_ts = int(df_final["ts"][0]) + (100 * 60 * 1000)
            end_time = start_ts
            time.sleep(0.1)  # avoid rate limits
        except Exception as error:
            print(f"error = {error}")

    df_final.drop_duplicates(inplace=True)
    df_final.sort_values(by=["datetime"], ascending=True, inplace=True)

    return df_final


if __name__ == "__main__":
    okx_client = Okx(
        OKX_MCA_MAIN_READ["api_key"],
        OKX_MCA_MAIN_READ["api_secret"],
        OKX_MCA_MAIN_READ["passphrase"],
    )
    candles = get_candles(okx_client)
