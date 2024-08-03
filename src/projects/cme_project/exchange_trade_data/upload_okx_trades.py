"""
download okx trades data
https://www.okx.com/data-download
"""

import os

import pandas as pd

from local_credentials.api_work.databases.postgres import SGTRD3_MARKETDATA_WRITE
from python.sg1_server.cronjobs.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def get_okx_trades():
    """
    download okx trades data
    saving raw data

    time_period:
        BRR - bitcoin reference rate 4pm london time +1 UTC (2pm to 3pm UTC)
        BRRNY - bitcoin reference rate 4pm new york time -4 UTC (7pm to 8pm UTC)
        BRRAP - bitcoin reference rate asia pacific 4pm hong kong time +8 UTC (7am to 8am UTC)

    """

    ### Fill in folder directory here ###
    okx_folder_directory = "D:/okx_data"

    df_final = pd.DataFrame()
    okx_headers = [
        "instrument_name",
        "trade_id",
        "side",
        "size",
        "price",
        "created_time",
    ]

    file_names = os.listdir(okx_folder_directory)
    for file in file_names:
        filepath = okx_folder_directory + "/" + file
        print(filepath)

        df_okx = pd.read_csv(filepath, encoding="unicode_escape", index_col=None)
        df_okx = df_okx.set_axis(okx_headers, axis=1)
        df_okx = df_okx.loc[df_okx["instrument_name"] == "ETH-USDT"]  ## instrument here
        df_okx.sort_values(by="created_time", inplace=True)
        df_okx["utc_datetime"] = pd.to_datetime(df_okx["created_time"], unit="ms")
        df_okx["hour"] = df_okx["utc_datetime"].dt.hour
        df_final = pd.concat([df_final, df_okx])

    df_final = df_final.loc[df_final["hour"].isin([7])]  # Filter trades
    df_final.loc[df_final["hour"] == 7, "reference"] = "BRRAP"
    return df_final


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    client.connect("postgres")

    # retrieve data
    data = get_okx_trades()
    print(data)

    # with client.engine.connect() as conn:
    #     data.to_sql(
    #         "okx_spot_ethusdt_trades",
    #         conn,
    #         if_exists="append",
    #         index=False,
    #     )
