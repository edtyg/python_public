"""
uploading bybit data
last row of data is not finalized - to exclude in each call
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


def get_bybit_data(
    symbol: str,
    interval: str,
    start_time: Optional[int] = None,
):
    """
    pulling bybit klines using rest API
    saving raw data

    symbol = 'BTCUSDT'
    interval = 1,3,5...
    """
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "spot",
        "symbol": symbol.upper(),
        "interval": interval,
        "start": start_time,
        "limit": 1000,  # max 1000 rows
    }
    response = requests.get(url=url, params=params, timeout=5)
    data = response.json()["result"]["list"]

    # ### saving data as pandas dataframe ###
    response_columns = [
        "ts",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "turnover",
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
    df_data.sort_values(by="utc_datetime", ascending=True, inplace=True)
    df_data.set_index("utc_datetime", inplace=True)
    df_data.drop(df_data.tail(1).index, inplace=True)  # drop last row

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
        # 1st jan 2024 12 am utc time
        ts = int(dt.datetime(2024, 5, 1, 8, 0, 0).timestamp() * 1000)
        df_data = get_bybit_data(symbol.upper(), interval, ts)
        df_data = df_data.head(1)

        with client.engine.connect() as conn:
            try:
                df_data.to_sql(
                    table_name,
                    conn,
                    if_exists="append",
                    index=True,
                )
            except Exception as e:
                print(e)
            print(f"{str(len(df_data))} added to table {table_name}")


def upload_latest_data(client, symbol: str, table_name: str, interval: str):
    """
    pulls time of latest data from database
    pulls data from exchange api

    symbol: BTCUSDT
    table_name: bybit_spot_btcusdt_1m
    interval: 60
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
        bybit_data = get_bybit_data(symbol, interval, latest_date)
        df_final = bybit_data.loc[bybit_data["ts"] > int(latest_date)]  # filters

        with client.engine.connect() as conn:
            try:
                df_final.to_sql(
                    table_name,
                    conn,
                    if_exists="append",
                    index=True,
                )
            except Exception as e:
                print(e)
        print(f"{str(len(df_final))} added to table {table_name}")
    except Exception as error:
        print(error)


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_2_MARKETDATA_WRITE)
    client.connect("postgres")

    # symbol = "btcusdt"
    symbol = sys.argv[1]
    table_name = f"bybit_spot_{symbol.lower()}_1m"
    interval = 1

    upload_latest_data(
        client,
        symbol=symbol,
        table_name=table_name,
        interval=interval,
    )
