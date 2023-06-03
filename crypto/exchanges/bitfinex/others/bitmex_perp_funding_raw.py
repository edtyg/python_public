import requests
import pandas as pd
import datetime as dt


def get_derivatives_status(symbol, start_time, end_time):
    url = f"https://api-pub.bitfinex.com/v2/status/deriv/{symbol}/hist"
    params = {
        "limit": 5000,
        "sort": 1,
        "start": start_time,
        "end": end_time,
    }  # sort 1 = oldest to newest
    response = requests.request("GET", url, headers={}, data={}, params=params)

    data = response.json()

    col_names = [
        "MTS",
        "PLACEHOLDER",
        "DERIV_PRICE",
        "SPOT_PRICE",
        "PLACEHOLDER",
        "INSURANCE_FUND_BALANCE",
        "PLACEHOLDER",
        "NEXT_FUNDING_EVT_TIMESTAMP_MS",
        "NEXT_FUNDING_ACCRUED",
        "NEXT_FUNDING_STEP",
        "PLACEHOLDER",
        "CURRENT_FUNDING",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "MARK_PRICE",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "OPEN_INTEREST",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "CLAMP_MIN",
        "CLAMP_MAX",
    ]

    df = pd.DataFrame(data, columns=col_names)
    df["MTS"] = pd.to_datetime(df["MTS"], unit="ms")  # miliseconds
    df.rename(columns={"MTS": "date"}, inplace=True)
    return df


if __name__ == "__main__":
    symbol = "tBTCF0:USTF0"
    start_time = int(
        dt.datetime(2021, 6, 1, 12, 0, 0).timestamp() * 1000
    )  # start time * 1000 -> milliseconds
    end_time = int(
        dt.datetime(2021, 6, 5, 12, 0, 0).timestamp() * 1000
    )  # end time * 1000 > milliseconds

    df_btc = get_derivatives_status(symbol, start_time, end_time)  # btc perp symbol
