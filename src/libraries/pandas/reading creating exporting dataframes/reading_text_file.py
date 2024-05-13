"""
read json file
"""

import json

import pandas as pd

if __name__ == "__main__":
    # BRTI - bitcoin real time index
    # BRR - bitcoin reference rate 4pm london time
    # BRRNY - bitcoin reference rate 4pm new york time
    # BRRAP - bitcoin reference rate asia pacific 4pm hong kong time
    data_filter = ["BRR", "BRRNY", "BRRAP"]

    save_path = "C:/Users/Administrator/OneDrive/Desktop/"
    filename = "20240324-CRYPTOCURRENCY_0_0_0_0"
    filepath = save_path + filename

    final_list = []
    with open(filepath, "r") as log_file:
        for line in log_file:
            dict_data = json.loads(line)
            try:
                entry = dict_data["mdEntries"][0]
                if entry["symbol"] in data_filter:
                    final_list.append(entry)
            except Exception as error:
                print(error)
                continue

    df_final = pd.DataFrame(final_list)
