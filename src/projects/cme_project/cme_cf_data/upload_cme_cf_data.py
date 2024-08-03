"""
uploading binance data
"""

import json
import os

import pandas as pd

from local_credentials.api_work.databases.postgres import SGTRD3_MARKETDATA_WRITE
from python.sg1_server.cronjobs.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def get_cme_data():
    """
    pulling binance klines using rest API
    saving raw data
    """
    # BRTI - bitcoin real time index
    # BRR - bitcoin reference rate 4pm london time
    # BRRNY - bitcoin reference rate 4pm new york time
    # BRRAP - bitcoin reference rate asia pacific 4pm hong kong time

    # BRTI - bitcoin real time index
    # BRR - bitcoin reference rate 4pm london time
    # BRRNY - bitcoin reference rate 4pm new york time
    # BRRAP - bitcoin reference rate asia pacific 4pm hong kong time

    # data_filter = ["BRR", "BRRNY", "BRRAP"]
    data_filter = ["ETHUSD_RR", "ETHUSD_NY", "ETHUSD_AP"]

    df_final = pd.DataFrame()
    cme_files_folder = "D:/CME_Data/2024"
    cme_unpacked_files = os.listdir(cme_files_folder)

    for file in cme_unpacked_files:
        filepath = cme_files_folder + "/" + file
        print(filepath)

        final_list = []
        with open(filepath, "r") as log_file:
            for line in log_file:
                try:
                    dict_data = json.loads(line)
                    entry = dict_data["mdEntries"][0]
                    if entry["symbol"] in data_filter:
                        final_list.append(entry)
                except Exception as error:
                    print(error)
                    continue

            df = pd.DataFrame(final_list)

        df_final = pd.concat([df_final, df])
        print(df_final)

    return df_final


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    client.connect("postgres")

    # retrieve data
    cme_data = get_cme_data()
    print(cme_data)

    with client.engine.connect() as conn:
        cme_data.to_sql(
            "cme_cf_ethusd",
            conn,
            if_exists="append",
            index=False,
        )
