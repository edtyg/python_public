import requests
import pandas as pd
import datetime as dt
import math


def bitfinex_perp_funding_rates(symbol, start_time, end_time):
    symbol_dict = {"tBTCF0:USTF0": "BTC", "tETHF0:USTF0": "ETH"}
    df_final = pd.DataFrame()
    diff = end_time - start_time
    call_max = 5000 * 60 * 1000  # 1000 rows * 60 seconds * 8 hrs * 1000 (milliseconds)

    start_iteration = start_time
    end_iteration = start_time + call_max

    num_iterations = math.floor(diff / call_max)  # number of loops required
    for i in range(num_iterations):
        print(i)
        url = f"https://api-pub.bitfinex.com/v2/status/deriv/{symbol}/hist?start={start_iteration}&end={end_iteration}&sort=1&limit=5000"
        response = requests.request("GET", url, headers={}, data={})
        data = response.json()

        time = []
        rate = []
        mark_price = []
        for i in data:
            time.append(i[0])
            rate.append(i[8])
            mark_price.append(i[14])

        df = pd.DataFrame({"time": time, "rate": rate, "mark_price": mark_price})
        df["date"] = pd.to_datetime(df["time"], unit="ms")  # miliseconds
        df["year"] = pd.DatetimeIndex(df["date"]).year
        df["month"] = pd.DatetimeIndex(df["date"]).month
        df["day"] = pd.DatetimeIndex(df["date"]).day
        df["hour"] = pd.DatetimeIndex(df["date"]).hour
        df = df.groupby(
            ["year", "month", "day", "hour"], as_index=False
        ).mean()  # groupby
        df_final = df_final.append(df)

        start_iteration = end_iteration
        end_iteration = start_iteration + call_max

        print(df_final)

    end_iteration = dt.datetime(2021, 1, 1).now().timestamp() * 1000
    url = f"https://api-pub.bitfinex.com/v2/status/deriv/{symbol}/hist?start={start_iteration}&end={end_iteration}&sort=1&limit=5000"
    response = requests.request("GET", url, headers={}, data={})
    data = response.json()

    time = []
    rate = []
    mark_price = []
    for i in data:
        time.append(i[0])
        rate.append(i[8])
        mark_price.append(i[14])

    df = pd.DataFrame({"time": time, "rate": rate, "mark_price": mark_price})
    df["date"] = pd.to_datetime(df["time"], unit="ms")  # miliseconds
    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["month"] = pd.DatetimeIndex(df["date"]).month
    df["day"] = pd.DatetimeIndex(df["date"]).day
    df["hour"] = pd.DatetimeIndex(df["date"]).hour
    df = df.groupby(["year", "month", "day", "hour"], as_index=False).mean()  # groupby
    df_final = df_final.append(df)

    df_final.reset_index(drop=True, inplace=True)
    df_final["apy"] = df_final["rate"] * 3 * 365
    df_final["symbol"] = symbol_dict[symbol]
    df_final["type"] = "bitfinex_usdm"
    df_final["exchange"] = "bitfinex"
    df_final.rename(columns={"rate": "fundingRate"}, inplace=True)
    df_final["date"] = pd.to_datetime(df_final[["year", "month", "day", "hour"]])
    df_final = df_final[["date", "symbol", "fundingRate", "apy", "type", "exchange"]]

    return df_final


def export_excel(list_of_pairs):
    writer = pd.ExcelWriter(save_path + filename)
    for i in list_of_pairs:
        df = bitfinex_perp_funding_rates(i, start_time, end_time)
        df.to_excel(writer, sheet_name=symbol[i] + " Funding Rates")

    writer.save()
    print("file Saved")


if __name__ == "__main__":
    save_path = "C:/Users/edgar tan/desktop/python outputs/"  # file path
    filename = "bitfinex_perp_funding.xlsx"  # filename

    start_time = int(
        dt.datetime(2021, 6, 1, 12, 0, 0).timestamp() * 1000
    )  # start time * 1000 -> milliseconds
    end_time = int(
        dt.datetime(2021, 6, 11, 12, 0, 0).timestamp() * 1000
    )  # end time * 1000 > milliseconds
    symbol = {"tBTCF0:USTF0": "BTC_PERP", "tETHF0:USTF0": "ETH_PERP"}

    export_excel(symbol)
