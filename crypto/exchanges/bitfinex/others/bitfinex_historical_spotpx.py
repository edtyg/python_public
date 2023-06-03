import requests
import pandas as pd
import datetime as dt
import math


def bitfinex_historical_spotpx(symbol, start_time, end_time):
    df_final = pd.DataFrame()
    diff = end_time - start_time
    call_max = 10000 * 3600 * 1000  # 10000 rows * 3600 * 1000 (milliseconds)

    start_iteration = start_time
    end_iteration = start_time + call_max

    num_iterations = math.floor(diff / call_max)  # number of loops required
    for i in range(num_iterations):
        url = f"https://api-pub.bitfinex.com/v2/candles/trade:1h:{symbol}/hist?limit=10000&start={start_iteration}&end={end_iteration}&sort=1"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()

        col = ["timestamp", "open", "close", "high", "low", "volume"]
        df = pd.DataFrame(data, columns=col)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # miliseconds
        df_final = df_final.append(df)

        start_iteration = end_iteration
        end_iteration = start_iteration + call_max

        print(df_final)

    # final iteration #
    end_iteration = dt.datetime(2021, 1, 1).now().timestamp() * 1000
    url = f"https://api-pub.bitfinex.com/v2/candles/trade:1h:{symbol}/hist?limit=10000&start={start_iteration}&end={end_iteration}&sort=1"
    response = requests.request("GET", url, headers={}, data={})
    data = response.json()

    col = ["timestamp", "open", "close", "high", "low", "volume"]
    df = pd.DataFrame(data, columns=col)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # miliseconds
    df_final = df_final.append(df)

    df_final.reset_index(drop=True, inplace=True)

    return df_final


def export_excel(list_of_pairs):
    writer = pd.ExcelWriter(save_path + filename)
    for i in list_of_pairs:
        df = bitfinex_historical_spotpx(i, start_time, end_time)
        df.to_excel(writer, sheet_name=i + " spot px")

    writer.save()
    print("file Saved")


if __name__ == "__main__":
    save_path = "C:/Users/edgar tan/desktop/python outputs/"  # file path
    filename = "bitfinex_spot_px.xlsx"  # filename

    start_time = int(
        dt.datetime(2020, 1, 1, 12, 0, 0).timestamp() * 1000
    )  # start time * 1000 -> milliseconds
    end_time = int(
        dt.datetime(2021, 5, 27, 12, 0, 0).timestamp() * 1000
    )  # end time * 1000 > milliseconds
    symbol = ["tUSTUSD"]  # usdt/usd symbol for bitfinex

    df = bitfinex_historical_spotpx("tUSTUSD", start_time, end_time)
    export_excel(symbol)
