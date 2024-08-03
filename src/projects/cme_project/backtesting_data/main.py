"""
pip install sqlalchemy
connecting to sql databases using sqlalchemy
creating tables for CME data

"""

import pandas as pd
from sqlalchemy import, text

from local_credentials.api_work.databases.postgres import SGTRD3_MARKETDATA_WRITE
from python.sg1_server.cronjobs.cme_project.backtesting_data.config_file import (
    k,
    weight,
)
from python.sg1_server.cronjobs.cme_project.sqlalchemy_library.sqlalchemy_client import (
    SqlAlchemyConnector,
)


def select_table(client, query: str):
    """Selects Table using a query string"""
    engine = client.engine
    connection = engine.connect()
    sql_query = text(query)
    result_proxy = connection.execute(sql_query)
    results = result_proxy.fetchall()
    df_results = pd.DataFrame(results)
    return df_results

def get_brrap_data(client):
    """Getting BRRAP Data - Pulls from cme_cf_brr table"""

    query = """
    Select * from cme_cf_brr
    where symbol = 'BRRAP'
    """
    df_data = select_table(client, query)
    return df_data


def get_ethusdap_data(client):
    """Getting ETHUSD_AP Data - Pulls from cme_cf_ethusd table"""

    query = """
    Select * from cme_cf_ethusd
    where symbol = 'ETHUSD_AP'
    """
    df_data = select_table(client, query)
    return df_data


def get_binance_data(client, date, type: str):
    """Getting Binance trade data
    type = "BTC" or "ETH
    binance_spot_btcusdt_trades
    binance_spot_ethusdt_trades
    """

    query = f"""
    Select * from binance_spot_{type.lower()}usdt_trades
    where Date(utc_datetime) = '{date}'
    """
    df_data = select_table(client, query)
    return df_data


def get_okx_data(client, date, type: str):
    """Getting Binance trade data
    type = "BTC" or "ETH
    okx_spot_btcusdt_trades
    okx_spot_ethusdt_trades
    """

    query = f"""
    Select * from okx_spot_{type.lower()}usdt_trades
    where Date(utc_datetime) = '{date}'
    """
    df_data = select_table(client, query)
    return df_data


def main(client, k, type: str):
    """Backtesting strategy
    type = "BTC" or "ETH"
    set k in params
    """

    if type.upper() == "BTC":
        df_data = get_brrap_data(client)
    elif type.upper() == "ETH":
        df_data = get_ethusdap_data(client)

    df_data["datetime"] = pd.to_datetime(df_data["mdEntryDate"], format="%Y%m%d")
    df_data = df_data.loc[
        (df_data["datetime"] <= "2024-03-31") & (df_data["datetime"] >= "2024-01-01")
    ]
    df_data["mdEntryPx"] = df_data["mdEntryPx"].astype("float")
    print(df_data)

    # loops through date of brrap index
    for i in df_data.index:
        date = df_data.loc[i, "datetime"]
        print(date)

        ################################
        ### get binance data by date ###
        ################################
        df_binance = get_binance_data(client, date, type)
        df_binance.sort_values(by="utc_datetime", inplace=True)
        df_binance.reset_index(drop=True, inplace=True)

        # creates a new column with k partitions
        seconds_elapsed = (
            (df_binance["utc_datetime"] - df_binance["utc_datetime"].dt.floor("H"))
            .dt.total_seconds()
            .astype(int)
        )
        time_interval = 3600 / k
        time_intervals_elapsed = (seconds_elapsed / time_interval).astype(int)
        df_binance["k_partitions"] = time_intervals_elapsed + 1
        print(df_binance)

        price_data = {}
        partition = 1
        while partition <= k:
            # print(f"working on partition {partition}")
            df_binance_partition = df_binance.loc[
                df_binance["k_partitions"] == partition
            ]
            partition_length = len(df_binance_partition)
            # print(f"length of partition {partition} = {partition_length}")

            if partition_length == 0:
                # print("No Trades done in this partition")
                partition += 1
                continue

            elif partition_length % 2 != 0:
                # odd number of trades
                row_data = dict(
                    df_binance_partition.iloc[int(partition_length / 2 - 1)]
                )
                price = float(row_data["price"])
                price_data[partition] = price

            elif partition_length % 2 == 0:
                # even number of trades
                row_data_a = dict(
                    df_binance_partition.iloc[int(partition_length + 1 / 2 - 1)]
                )
                row_data_b = dict(
                    df_binance_partition.iloc[int(partition_length - 1 / 2 - 1)]
                )
                price = (float(row_data_a["price"]) + float(row_data_b["price"])) / 2
                price_data[partition] = price

            partition += 1

        price_binance = sum(price_data.values()) / len(price_data.values())
        print(f"binance price = {price_binance}")

        ############################
        ### get okx data by date ###
        ############################
        df_okx = get_okx_data(client, date, type)
        df_okx.sort_values(by="utc_datetime", inplace=True)
        df_okx.reset_index(drop=True, inplace=True)

        # creates a new column with k partitions
        seconds_elapsed = (
            (df_okx["utc_datetime"] - df_okx["utc_datetime"].dt.floor("H"))
            .dt.total_seconds()
            .astype(int)
        )
        time_interval = 3600 / k
        time_intervals_elapsed = (seconds_elapsed / time_interval).astype(int)
        df_okx["k_partitions"] = time_intervals_elapsed + 1
        print(df_okx)

        price_data = {}
        partition = 1
        while partition <= k:
            # print(f"working on partition {partition}")
            df_okx_partition = df_okx.loc[df_okx["k_partitions"] == partition]
            partition_length = len(df_okx_partition)
            # print(f"length of partition {partition} = {partition_length}")

            if partition_length == 0:
                # print("No Trades done in this partition")
                partition += 1
                continue

            elif partition_length % 2 != 0:
                # odd number of trades
                row_data = dict(df_okx_partition.iloc[int(partition_length / 2 - 1)])
                price = float(row_data["price"])
                price_data[partition] = price

            elif partition_length % 2 == 0:
                # even number of trades
                row_data_a = dict(
                    df_okx_partition.iloc[int(partition_length + 1 / 2 - 1)]
                )
                row_data_b = dict(
                    df_okx_partition.iloc[int(partition_length - 1 / 2 - 1)]
                )
                price = (float(row_data_a["price"]) + float(row_data_b["price"])) / 2
                price_data[partition] = price
            partition += 1

        price_okx = sum(price_data.values()) / len(price_data.values())
        print(f"okx price = {price_okx}")

        ########################
        ### applying weights ###
        ########################

        if sum(weight.values()) != 1:
            print("check weights - does not sum to 1")
        weighted_price = weight["Binance"] * price_binance + weight["Okx"] * price_okx

        df_data.loc[i, "number_partitions"] = k
        df_data.loc[i, "binance_weight"] = weight["Binance"]
        df_data.loc[i, "okx_weight"] = weight["Okx"]
        df_data.loc[i, "binance_price"] = price_binance
        df_data.loc[i, "okx_price"] = price_okx
        df_data.loc[i, "weighted_price"] = weighted_price
        df_data.loc[i, "px_diff"] = (
            df_data.loc[i, "weighted_price"] - df_data.loc[i, "mdEntryPx"]
        )
        df_data.loc[i, "px_diff_pct"] = (
            (df_data.loc[i, "weighted_price"] / df_data.loc[i, "mdEntryPx"]) - 1
        ) * 100

    return df_data


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    client.connect("postgres")

    # data = get_brrap_data(client)
    # print(data)

    # df_binance = get_binance_data(client, "2024-01-01", "ETH")
    # print(df_binance)

    # df_okx = get_okx_data(client, "2024-01-01", "ETH")
    # print(df_okx)

    ### btc back test ###
    # btc_data = main(client, k, "BTC")
    # writer = pd.ExcelWriter("D:/CME_Data/output_btc.xlsx")
    # btc_data.to_excel(writer, sheet_name="btc_backtest", index=False)
    # writer.close()

    ### eth back test ###
    eth_data = main(client, k, "ETH")
    writer = pd.ExcelWriter("D:/CME_Data/output_eth.xlsx")
    eth_data.to_excel(writer, sheet_name="eth_backtest", index=False)
    writer.close()
