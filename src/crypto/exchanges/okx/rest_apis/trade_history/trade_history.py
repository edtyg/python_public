"""
SPOT execution program
"""

import datetime as dt
import time
from typing import Optional

import pandas as pd

from local_credentials.api_work.crypto_exchanges.okx import (
    OKX_MCA_LTP1_READ,
    OKX_MCA_MAIN_READ,
)
from python.crypto.exchanges.okx.rest.okx_client import Okx


# get_transaction_details_3m
def get_trade_records(
    client,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
):
    """Gets trade records up to 3 months

    Args:
        client (_type_): okx spot client
    """
    df_trades_final = pd.DataFrame()
    trade_status = False

    while trade_status is False:
        params = {
            "instType": "SPOT",
            "end": end_time,
            "limit": 100,
        }
        trades = client.get_transaction_details_3m(params)
        df_trades = pd.DataFrame(trades["data"])
        print(df_trades)

        # gets earliest time from final df
        try:
            current_earliest_time = df_trades_final.tail(1)["ts"].values[0]
        except Exception as e:
            current_earliest_time = end_time
            print(e)

        # filters newly pulled df by earliest time
        try:
            df_trades["ts"] = df_trades["ts"].astype("float")
            df_trades = df_trades.loc[df_trades["ts"] < current_earliest_time]
        except Exception as e:
            print(e)

        # filters orders greater than latest time
        if df_trades.empty is True:
            trade_status = True
            continue
        else:
            df_trades_final = pd.concat([df_trades_final, df_trades])
            earliest_time = df_trades_final.tail(1)["ts"].values[0]
            end_time = int(earliest_time)

        if end_time < start_time:
            trade_status = True
            continue

        time.sleep(0.1)

    if df_trades_final.empty is True:
        return df_trades_final
    else:
        df_trades_final["datetime"] = pd.to_datetime(df_trades_final["ts"], unit="ms")
        return df_trades_final


def request_trade_records_2y(client, year: str, quarter: str):
    """Post request for trade records in the past 2 years
    by quarter
    use get request below to retrieve link to download csv file

    Args:
        client (_type_): okx spot client
    """
    params = {
        "year": year,
        "quarter": quarter,
    }
    trades = client.post_transaction_details_2y(params)
    return trades


def retrieve_trade_records_2y(client, year: str, quarter: str):
    """Gets link to download trade records
    used in conjunction with the above

    Args:
        client (_type_): okx spot client
    """
    params = {
        "year": year,
        "quarter": quarter,
    }
    trades = client.get_transaction_details_2y(params)
    return trades


if __name__ == "__main__":
    key = OKX_MCA_LTP1_READ
    okx_client = Okx(
        apikey=key["api_key"],
        apisecret=key["api_secret"],
        passphrase=key["passphrase"],
    )

    # start_time = int(dt.datetime(2024, 1, 25, 12, 0, 0).timestamp() * 1000)
    # end_time = int(dt.datetime(2024, 1, 29, 12, 0, 0).timestamp() * 1000)
    # trade_records = get_trade_records(okx_client, start_time, end_time)
    # print(trade_records)

    # req = request_trade_records_2y(okx_client, "2023", "Q1")
    # ret = retrieve_trade_records_2y(okx_client, "2023", "Q1")

    tx_details_3d = okx_client.get_transaction_details_3d(
        {
            "instType": "SPOT",
            "ordId": None,
            "instId": "BTC-USDT",
        }
    )
    print(tx_details_3d)
