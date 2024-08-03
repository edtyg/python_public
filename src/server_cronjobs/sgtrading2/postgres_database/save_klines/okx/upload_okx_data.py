"""
uploading okx data
okx kline api different from binance
latest row finalized - unlike binance
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


def get_okx_data(
    instrument_id: str,
    interval: str,
    start_time: Optional[int] = None,
):
    """
    pulling binance klines using rest API
    saving raw data

    after: pulls data before stated timestamp
    before: pulls latest data after stated timestamp but must be
    within 100 rows - if not it pulls latest 100 rows

    instrument_id = "BTC-USDT
    start_time = 1704038400000
    interval = "1h", "1m", ...
    """
    url = "https://www.okx.com/api/v5/market/history-candles"
    if interval == "1h":
        params = {
            "instId": instrument_id.upper(),
            "bar": interval,
            "before": start_time,
            "after": start_time
            + 100 * 60 * 60 * 1000,  # 100rows * 3600seconds * 1000ms
            "limit": 100,  # max 100 rows
        }
    elif interval == "1m":
        params = {
            "instId": instrument_id.upper(),
            "bar": interval,
            "before": start_time,
            "after": start_time + 100 * 60 * 1000,  # 100rows * 60seconds * 1000ms
            "limit": 100,  # max 100 rows
        }
    response = requests.get(url=url, params=params, timeout=5)
    data = response.json()["data"]

    ### saving data as pandas dataframe ###
    response_columns = [
        "ts",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "volccy",
        "volccyquote",
        "confirm",
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
    print(df_results)
    if not df_results.empty:
        print("table has data")
    else:
        print("table has no data")
        # initial upload
        # 1st jan 2024 12 am utc time
        ts = int(dt.datetime(2024, 5, 1, 8, 0, 0).timestamp() * 1000)
        df_data = get_okx_data(symbol.upper(), interval, ts)
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
    upload data into DB

    symbol: BTC-USDT
    table_name: okx_spot_btcusdt_1m
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
    print(df_results)

    try:
        latest_date = max(df_results["ts"])  # gets latest date
        okx_data = get_okx_data(symbol.upper(), interval, latest_date)
        print(okx_data)
        df_final = okx_data.loc[okx_data["ts"] > latest_date]

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

    # symbol = "eth-usdt"
    symbol = sys.argv[1]

    table_name = f"okx_spot_{symbol.replace('-', '')}_1m"
    interval = "1m"

    upload_latest_data(
        client,
        symbol=symbol,
        table_name=table_name,
        interval="1m",
    )
