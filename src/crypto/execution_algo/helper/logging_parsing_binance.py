"""
Created on Sat Aug 19 23:11:04 2023

@author: Edgar Tan
"""

import ast
import pandas as pd

if __name__ == "__main__":
    # log file directory
    log_file_path = "C:/Users/EdgarTan/Documents/Github/python/libraries/logging/"
    log_file_name = "29_04_2024_market_order_brrap_live"
    log_file = log_file_path + log_file_name + ".log"

    # exporting excel file
    excel_file_path = log_file_path
    excel_file_name = log_file_name
    excel_file = excel_file_path + excel_file_name + ".xlsx"
    writer = pd.ExcelWriter(excel_file)

    # loops through log file appends messages that we're able to split
    msg_data = []
    with open(log_file, "r") as log_file:
        for line in log_file:
            try:
                msg_split = line.split("|")
                message = msg_split[5]
                msg_data.append(message)
            except Exception as e:
                print(e)

    # loops through data and filters out messages
    data_parsed = []
    for msg in msg_data:
        try:
            parsing_msg = msg[4:]
            data_dict = ast.literal_eval(parsing_msg)
            data_parsed.append(data_dict)
        except Exception as e:
            print(e)

    # appends as dataframe
    df_data_fills = pd.DataFrame()
    for dict_data in data_parsed:
        try:
            transact_time = dict_data["transactTime"]
            order_id = dict_data["orderId"]
            symbol = dict_data["symbol"]
            client_id = dict_data["clientOrderId"]
            fills = dict_data["fills"]

            df_data = pd.DataFrame(fills)
            df_data["transact_time"] = transact_time
            df_data["order_id"] = order_id
            df_data["symbol"] = symbol
            df_data["client_id"] = client_id

            df_data_fills = pd.concat([df_data_fills, df_data])

        except Exception as e:
            print(e)
            continue

    # final adjustments
    df_data_fills["datetime"] = pd.to_datetime(
        df_data_fills["transact_time"], unit="ms"
    )

    df_data_fills["price"] = df_data_fills["price"].astype("float")
    df_data_fills["qty"] = df_data_fills["qty"].astype("float")

    df_data_fills["volume"] = df_data_fills["price"] * df_data_fills["qty"]

    # exports to excel
    df_data_fills.to_excel(writer, sheet_name="binance_trade_logs", index=False)
    writer.close()
    print("file Saved")
