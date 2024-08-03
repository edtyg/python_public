"""
uploading coinbase data
latest row not finalized
"""

import datetime as dt
import sys
import time
from typing import Optional

import pandas as pd
import requests
from sqlalchemy import text

from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN
from src.projects.postgres_database.connection_client import SqlAlchemyConnector


def get_coinbase_data(
    product_id: str,
    interval: int,
    start_time: int,
):
    """
    pulling coinbase klines using rest API
    saving raw data

    product_id = 'BTC-USDT'
    granularity = 60, 300,...
    """
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"

    params = {
        "granularity": str(interval),
        "start": start_time,
        "end": start_time + (300 * interval),  # 300 rows max
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
    ]
    df_data = pd.DataFrame(data, columns=response_columns)
    df_data["ts"] = (df_data["ts"] * 1000).astype("int64")
    df_data["utc_datetime"] = pd.to_datetime(df_data["ts"], unit="ms")
    df_data = df_data.sort_values(by="utc_datetime", ascending=True)
    df_data.set_index("utc_datetime", inplace=True)
    df_data.drop(df_data.tail(1).index, inplace=True)  # drop last row after sorting
    return df_data


def upload_initial_data(client, symbol: str, table_name: str, interval: int):
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
        ts = int(dt.datetime(2024, 5, 12, 8, 0, 0).timestamp())
        df_data = get_coinbase_data(symbol.upper(), interval, ts)
        df_data = df_data.tail(1)

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


def upload_latest_data(client, symbol: str, table_name: str, interval: int):
    """
    pulls time of latest data from database
    pulls data from exchange api

    symbol: BTC-USD
    table_name: coinbase_spot_btcusd_1m
    interval: 60
    """

    query = f"""
    SELECT *
    FROM {table_name}
    ORDER BY utc_datetime DESC
    LIMIT 1;
    """
    # uploads initial data if table is empty
    upload_initial_data(client, symbol, table_name, interval)

    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()
    df_results = pd.DataFrame(results)

    try:
        latest_date = max(df_results["ts"])  # gets latest row by date
        print(latest_date)
        coinbase_data = get_coinbase_data(symbol, interval, int(latest_date / 1000))
        print(coinbase_data)
        df_final = coinbase_data.loc[coinbase_data["ts"] > int(latest_date)]  # filters
        print(df_final)
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
    client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    client.connect("postgres")

    symbol = "btc-usd"
    table_name = f"coinbase_spot_{symbol.replace('-', '')}_1m"
    interval = 60

    # set cronjob to run by minute but sleep for a few seconds
    # offset time delay on exchange side if any
    time.sleep(5)
    upload_latest_data(
        client,
        symbol=symbol,
        table_name=table_name,
        interval=interval,
    )
