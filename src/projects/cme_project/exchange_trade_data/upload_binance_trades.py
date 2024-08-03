"""
download binance trades data
https://www.binance.com/en/landing/data
"""

import pandas as pd

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def get_binance_trades():
    """
    download binance trades data
    saving raw data

    time_period:
        BRR - bitcoin reference rate 4pm london time +1 UTC (2pm to 3pm UTC)
        BRRNY - bitcoin reference rate 4pm new york time -4 UTC (7pm to 8pm UTC)
        BRRAP - bitcoin reference rate asia pacific 4pm hong kong time +8 UTC (7am to 8am UTC)

    """

    ### Fill in file path here ###
    binance_file = "D:/binance_data/ETHUSDT-trades-2024-01.csv"

    binance_headers = [
        "id",
        "price",
        "qty",
        "quote_qty",
        "time",
        "is_buyer_maker",
        "is_best_match",
    ]

    df_binance = pd.read_csv(binance_file, names=binance_headers, index_col=None)
    df_binance["utc_datetime"] = pd.to_datetime(df_binance["time"], unit="ms")
    df_binance["hour"] = df_binance["utc_datetime"].dt.hour
    df_binance = df_binance.loc[df_binance["hour"].isin([7])]  # Filter trades
    df_binance.loc[df_binance["hour"] == 7, "reference"] = "BRRAP"

    # table type
    df_binance["id"] = df_binance["id"].astype("int64")
    df_binance["price"] = df_binance["price"].astype("float")
    df_binance["qty"] = df_binance["qty"].astype("float")
    df_binance["quote_qty"] = df_binance["quote_qty"].astype("float")
    df_binance["time"] = df_binance["time"].astype("int64")
    df_binance["is_buyer_maker"] = df_binance["is_buyer_maker"].astype("bool")
    df_binance["is_best_match"] = df_binance["is_best_match"].astype("bool")
    df_binance["hour"] = df_binance["hour"].astype("int")
    df_binance["reference"] = df_binance["reference"].astype("str")

    df_binance.set_index("utc_datetime", inplace=True)
    return df_binance


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    client.connect("postgres")

    data = get_binance_trades()
    print(data)

    with client.engine.connect() as conn:
        data.to_sql(
            "binance_spot_ethusdt_trades_ht",
            conn,
            if_exists="append",
            index=True,
        )
