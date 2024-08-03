"""
Calculation of spot index
"""

import datetime as dt
import os

import pandas as pd
from sqlalchemy import text

from keys.api_work.databases.postgres import SG_TRADING_2_MARKETDATA_WRITE
from src.projects.spot_index_calculation.connection_client import SqlAlchemyConnector


def select_table(client, table_name, start_time, end_time):
    """
    selects table using sql client
    """
    client.connect("postgres")

    query = text(
        f"""
        SELECT * from {table_name}
        where utc_datetime >= '{start_time}' and utc_datetime < '{end_time}'
        """
    )
    print(query)

    connection = client.engine.connect()
    result_proxy = connection.execute(query)
    result = result_proxy.fetchall()
    df_result = pd.DataFrame(result)
    return df_result


def main(client, base_ccy, quote_ccy, start_time, end_time, client_direction, spreads):
    """
    Retrieves kline data from postgres tables
    calculates index price based on data

    Args:
        ccy: str - currency either "btc" or "eth"
        start_time
        end_time
        client_direction str - either 'buy' or 'sell'
        spreads - in bps
    """
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    output_excel = "spot_index_data.xlsx"
    writer = pd.ExcelWriter(save_path + output_excel)

    # dict to save df for exports
    excel_files = {}

    # query from postgres database
    ccy = base_ccy.lower()
    table_names = {
        f"binance_{ccy}usdt": f"binance_spot_{ccy}usdt_1m",
        f"bybit_{ccy}usdt": f"bybit_spot_{ccy}usdt_1m",
        f"okx_{ccy}usdt": f"okx_spot_{ccy}usdt_1m",
        f"coinbase_{ccy}usd": f"coinbase_spot_{ccy}usd_1m",
    }

    # to merge all the tables
    df_calculations = pd.DataFrame()

    # gets coinbase close price
    df_coinbase = select_table(client, "coinbase_spot_usdtusd_1m", start_time, end_time)
    df_coinbase = df_coinbase.tail(1)

    # coinbase USDT/USD rate
    coinbase_close_price = float(df_coinbase["close"].values[0])

    for key, value in table_names.items():
        df_result = select_table(client, value, start_time, end_time)

        if key.endswith("usdt") and quote_ccy.lower() == "usd":
            df_result["usd_conversion_rate"] = coinbase_close_price
            df_result["open_px_converted"] = (
                df_result["open"] * df_result["usd_conversion_rate"]
            )
        elif key.endswith("usdt") and quote_ccy.lower() == "usdt":
            df_result["usd_conversion_rate"] = 1
            df_result["open_px_converted"] = (
                df_result["open"] * df_result["usd_conversion_rate"]
            )
        elif key.endswith("usd") and quote_ccy.lower() == "usd":
            df_result["usd_conversion_rate"] = 1
            df_result["open_px_converted"] = (
                df_result["open"] * df_result["usd_conversion_rate"]
            )
        elif key.endswith("usd") and quote_ccy.lower() == "usdt":
            df_result["usd_conversion_rate"] = 1 / coinbase_close_price
            df_result["open_px_converted"] = (
                df_result["open"] * df_result["usd_conversion_rate"]
            )

        # saves individual table data into separate excel sheets
        df_result.to_excel(writer, sheet_name=value, index=False)
        # excel_files[value] = df_result

        # filters open price and volume from various tables except coinbase usdt usd
        df_result = df_result[["utc_datetime", "open_px_converted", "volume"]]
        df_result.rename(
            columns={
                "open_px_converted": f"{key}_openpx_converted",
                "volume": f"{key}_volume",
            },
            inplace=True,
        )
        if df_calculations.empty:
            df_calculations = df_result
        else:
            df_calculations = pd.merge(df_calculations, df_result, on="utc_datetime")

    # does calculations on df_summary
    # calculates total traded volume per row
    columns_volume = []
    for key in table_names.keys():
        column_name = key + "_volume"
        columns_volume.append(column_name)
    df_calculations["total_traded_volume"] = df_calculations[columns_volume].sum(axis=1)

    # calculates vwap price per row
    for i in df_calculations.index:
        vwap_price = 0
        for key in table_names.keys():
            total_traded_volume = df_calculations.loc[i, "total_traded_volume"]
            price = df_calculations.loc[i, f"{key}_openpx_converted"]
            volume = df_calculations.loc[i, f"{key}_volume"]
            price = (volume / total_traded_volume) * price
            vwap_price += price
        df_calculations.loc[i, "vwap_price"] = vwap_price

    average_vwap_price = df_calculations["vwap_price"].mean()
    avg_row = pd.DataFrame({"vwap_price": [average_vwap_price]})
    df_calculations = pd.concat([df_calculations, avg_row], ignore_index=True)

    # saves to excel
    df_calculations.to_excel(writer, sheet_name="calculations", index=False)
    # excel_files["calculations"] = df_calculations

    # calculates summary
    if client_direction == "buy":
        client_price = average_vwap_price * (1 + (spreads / 10000))
    elif client_direction == "sell":
        client_price = average_vwap_price * (1 - (spreads / 10000))
    else:
        print("please check direction")
        return

    df_summary = pd.DataFrame(
        {
            "usdt_usd_reference_price": coinbase_close_price,
            "calculated_reference_price": average_vwap_price,
            "client_direction": client_direction,
            "spread": spreads,
            "final_price_client": client_price,
        },
        index=[0],
    )
    df_summary.to_excel(writer, sheet_name="summary", index=False)
    excel_files["summary"] = df_summary

    print(excel_files)
    writer.close()
    print("file Saved")


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_2_MARKETDATA_WRITE)

    # Set parameters here
    base_ccy = "eth"
    quote_ccy = "usdt"
    client_direction = "sell"
    bps_spread = 30
    start_time = dt.datetime(2024, 5, 23, 7, 0, 0)
    end_time = dt.datetime(2024, 5, 23, 8, 0, 0)

    main(
        client, base_ccy, quote_ccy, start_time, end_time, client_direction, bps_spread
    )
