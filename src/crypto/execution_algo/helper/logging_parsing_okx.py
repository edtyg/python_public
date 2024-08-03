"""
Created on Sat Aug 19 23:11:04 2023

@author: Edgar Tan
"""

import ast
import pandas as pd

if __name__ == "__main__":
    # log file directory
    log_file_path = "C:/Users/EdgarTan/Documents/Github/python/libraries/logging/"
    log_file_name = "29042024brrap"
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
        fills = dict_data["data"]
        try:
            check_fills = fills[0]["side"]
            df_data = pd.DataFrame(fills)
            df_data_fills = pd.concat([df_data_fills, df_data])
        except Exception as error:
            continue

    # adds in datetime and calculates volume
    df_data_fills["datetime"] = pd.to_datetime(df_data_fills["fillTime"], unit="ms")
    df_data_fills["fillSz"] = df_data_fills["fillSz"].astype("float")
    df_data_fills["fillPx"] = df_data_fills["fillPx"].astype("float")
    df_data_fills["volume"] = df_data_fills["fillSz"] * df_data_fills["fillPx"]

    # exports to excel
    df_data_fills.to_excel(writer, sheet_name="okx_trade_logs", index=False)
    writer.close()
    print("file Saved")
