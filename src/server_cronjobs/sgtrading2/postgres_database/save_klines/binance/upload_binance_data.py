"""
uploading binance data
do not include latest row for binance as data is not finalized
offset last row for each call
"""

import datetime as dt
import sys
from typing import Optional

import pandas as pd
import requests
from sqlalchemy import text

from keys.api_work.databases.postgres import SG_TRADING_2_MARKETDATA_WRITE
from src.server_cronjobs.sgtrading2.postgres_database.connection_client import (
    SqlAlchemyConnector,
)


def get_binance_data(
    symbol: str,
    interval: str,
    start_time: Optional[int] = None,
):
    """
    pulling binance klines using rest API
    saving raw data
    interval = "1h", "1m", ...
    """
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "startTime": start_time,
        "limit": 1000,  # max rows per call = 1000
    }
    response = requests.get(url=url, params=params, timeout=5)
    data = response.json()

    ### saving data as pandas dataframe ###
    response_columns = [
        "ts",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]
    df_data = pd.DataFrame(data, columns=response_columns)

    # format column type
    df_data["ts"] = df_data["ts"].astype("int64")
    df_data["open"] = df_data["open"].astype("float")
    df_data["high"] = df_data["high"].astype("float")
    df_data["low"] = df_data["low"].astype("float")
    df_data["close"] = df_data["close"].astype("float")
    df_data["volume"] = df_data["volume"].astype("float")

    # creates datetime column and sorts
    df_data["utc_datetime"] = pd.to_datetime(df_data["ts"], unit="ms")
    df_data = df_data.sort_values(by="utc_datetime", ascending=True)
    df_data.set_index("utc_datetime", inplace=True)
    df_data.drop(df_data.tail(1).index, inplace=True)  # drop last row - data nt final

    # keep selected columns
    df_data = df_data[["ts", "open", "high", "low", "close", "volume"]]

    return df_data


def upload_initial_data(client, symbol: str, table_name: str, interval: str):
    """
    Uploads initial data if table is empty
    """

    query = f"""
    SELECT *
    FROM {table_name}
    ORDER BY utc_datetime DESC
    LIMIT 1;
    """

    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()
    df_results = pd.DataFrame(results)

    if not df_results.empty:
        print("table has data")
    else:
        print("table has no data")
        # initial upload
        ts = int(dt.datetime(2024, 5, 1, 8, 0, 0).timestamp() * 1000)
        df_data = get_binance_data(symbol.upper(), interval, ts)
        df_data = df_data.head(1)
        print(df_data)

        with client.engine.connect() as conn:
            try:
                df_data.to_sql(
                    table_name,
                    conn,
                    if_exists="append",
                    index=True,
                )
                print(f"{str(len(df_data))} added to table {table_name}")
            except Exception as e:
                print(e)


def upload_latest_data(client, symbol: str, table_name: str, interval: str):
    """
    pulls time of latest data from database
    pulls klines from binance after latest data in DB
    upload data into DB

    symbol: BTCUSDT
    table_name: binance_spot_btcusdt_1m
    interval: 1m
    """

    # uploads initial data if table is empty
    upload_initial_data(client, symbol, table_name, interval)

    query = f"""
    SELECT *
    FROM {table_name}
    ORDER BY utc_datetime DESC
    LIMIT 1;
    """

    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()
    df_results = pd.DataFrame(results)

    try:
        latest_date = max(df_results["ts"])  # gets latest row by date
        binance_data = get_binance_data(symbol.upper(), interval, latest_date)
        df_final = binance_data.loc[binance_data["ts"] > latest_date]  # filters

        with client.engine.connect() as conn:
            try:
                df_final.to_sql(
                    table_name,
                    conn,
                    if_exists="append",
                    index=True,
                )
                print(f"{str(len(df_final))} added to table {table_name}")
            except Exception as e:
                print(e)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_2_MARKETDATA_WRITE)
    client.connect("postgres")

    # symbol = "btcusdt"
    ohlcv_symbol = sys.argv[1]
    table_name = f"binance_spot_{symbol}_1m"
    ohlcv_interval = "1m"

    upload_latest_data(
        client,
        symbol=ohlcv_symbol,
        table_name=table_name,
        interval=ohlcv_interval,
    )
