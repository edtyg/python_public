from connection_client import conn_sqlalchemy
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

from fas_connection_credentials import fas_conn_credentials
from fas_utilities import get_fas_conn
import fas_database


def pull_data(conn_sqlalchemy):
    # pulling binance reserves data
    query = """
    select * from exchange_por where exchange = 'OKX'
    """
    data = conn_sqlalchemy.engine.execute(query).fetchall()
    return data


def get_table_in_df(conn, query):
    # for pulling data from fas mysql tables
    cursor = conn.cursor()
    cursor.execute(query)

    desc = cursor.description
    data = cursor.fetchall()

    headers = []
    for i in desc:
        headers.append(i[0])
    print(headers)

    df = pd.DataFrame(data, columns=headers)
    return df


def get_market_prices(conn, start_time, end_time):
    # gives some leeway to start and end time
    time_ahead = end_time + dt.timedelta(minutes=1)
    time_behind = start_time + dt.timedelta(minutes=-1)

    start_time = time_behind.strftime("%Y-%m-%d %H:%M:%S")
    end_time = time_ahead.strftime("%Y-%m-%d %H:%M:%S")

    query = f"""
    SELECT * from market_last_price_history
    where symbol_type = 'Spot'
    and snapshot_time >= '{start_time}'
    and snapshot_time <= '{end_time}'
    and std_symbol in ('BTC_USD', 'ETH_USD', 'BUSD_USD', 'USDT_USD', 'USDC_USD')
    """
    data = get_table_in_df(conn, query)
    return data


if __name__ == "__main__":
    # pulling exchange proof of reserves data - data captured every 5mins
    data = pull_data(conn_sqlalchemy.engine)
    df_por = pd.DataFrame(data)
    df_por.drop(columns=["index"], inplace=True)

    # creating ticker symbol
    df_por["ticker"] = df_por["coin"] + "_USD"

    # creates individual cols - require datetime format
    df_por["year"] = pd.DatetimeIndex(df_por["date"]).year
    df_por["month"] = pd.DatetimeIndex(df_por["date"]).month
    df_por["day"] = pd.DatetimeIndex(df_por["date"]).day
    df_por["hour"] = pd.DatetimeIndex(df_por["date"]).hour
    df_por["minute"] = pd.DatetimeIndex(df_por["date"]).minute
    df_por["second"] = pd.DatetimeIndex(df_por["date"]).second

    ## aggregate data by hour and by ticker - so use average of 5min data over 1 hour ##
    df_por = df_por.groupby(
        ["year", "month", "day", "hour", "ticker", "coin"], as_index=False
    ).mean()

    # pulling prices from fas - select a wide enough range
    conn = get_fas_conn(fas_conn_credentials)
    start_time = dt.datetime(2022, 12, 1, 0, 0, 0)
    end_time = dt.datetime(2023, 3, 31, 23, 0, 0)
    market_prices = get_market_prices(conn, start_time, end_time)

    market_prices["year"] = pd.DatetimeIndex(market_prices["snapshot_time"]).year
    market_prices["month"] = pd.DatetimeIndex(market_prices["snapshot_time"]).month
    market_prices["day"] = pd.DatetimeIndex(market_prices["snapshot_time"]).day
    market_prices["hour"] = pd.DatetimeIndex(market_prices["snapshot_time"]).hour

    market_prices = market_prices[
        [
            "last_price",
            "std_symbol",
            "year",
            "month",
            "day",
            "hour",
        ]
    ]

    # matching prices over to reserves
    df_final = pd.merge(
        df_por,
        market_prices,
        how="left",
        left_on=[
            "ticker",
            "year",
            "month",
            "day",
            "hour",
        ],
        right_on=[
            "std_symbol",
            "year",
            "month",
            "day",
            "hour",
        ],
    )
    df_final["final_balance"] = df_final["final_balance"].astype("float")
    df_final["last_price"] = df_final["last_price"].astype("float")

    df_final["market_cap"] = df_final["final_balance"] * df_final["last_price"]

    # regenerate date
    for i in df_final.index:
        year = df_final.loc[i, "year"]
        month = df_final.loc[i, "month"]
        day = df_final.loc[i, "day"]
        hour = df_final.loc[i, "hour"]
        df_final.loc[i, "date"] = dt.datetime(year, month, day, hour, 0, 0)

    # filtering out by coin
    df_btc = df_final.loc[df_por["coin"] == "BTC"]
    df_eth = df_final.loc[df_por["coin"] == "ETH"]
    df_busd = df_final.loc[df_por["coin"] == "BUSD"]
    df_usdt = df_final.loc[df_por["coin"] == "USDT"]
    df_usdc = df_final.loc[df_por["coin"] == "USDC"]

    ### btc reserves ###
    df_btc.plot(x="date", y="final_balance")
    plt.xlabel("Date", size=5)
    plt.ylabel("Balance", size=5)
    plt.title("OKX BTC Reserves", size=10)

    ### eth reserves ###
    df_eth.plot(x="date", y="final_balance")
    plt.xlabel("Date", size=5)
    plt.ylabel("Balance", size=5)
    plt.title("OKX ETH Reserves", size=10)

    ### busd reserves ###
    df_busd.plot(x="date", y="final_balance")
    plt.xlabel("Date", size=5)
    plt.ylabel("Balance", size=5)
    plt.title("OKX BUSD Reserves", size=10)

    ### usdt reserves ###
    df_usdt.plot(x="date", y="final_balance")
    plt.xlabel("Date", size=5)
    plt.ylabel("Balance", size=5)
    plt.title("OKX USDT Reserves", size=10)

    ### usdc reserves ###
    df_usdc.plot(x="date", y="final_balance")
    plt.xlabel("Date", size=5)
    plt.ylabel("Balance", size=5)
    plt.title("OKX USDC Reserves", size=10)

    ### total reserves m2m ###
    df_total_reserves_m2m = df_final.groupby(
        ["year", "month", "day", "hour"], as_index=False
    ).sum()
    df_total_reserves_m2m = df_total_reserves_m2m.loc[
        df_total_reserves_m2m["market_cap"] != 0
    ]
    for i in df_total_reserves_m2m.index:
        year = df_total_reserves_m2m.loc[i, "year"]
        month = df_total_reserves_m2m.loc[i, "month"]
        day = df_total_reserves_m2m.loc[i, "day"]
        hour = df_total_reserves_m2m.loc[i, "hour"]
        df_total_reserves_m2m.loc[i, "date"] = dt.datetime(year, month, day, hour, 0, 0)

    df_total_reserves_m2m.plot(x="date", y="market_cap")
    plt.xlabel("Date", size=5)
    plt.ylabel("Marketcap", size=5)
    plt.title("OKX Reserves Total Marketcap", size=10)

    ### total reserves btc eth m2m
    df_final_btc_eth = df_final.loc[df_final["coin"].isin(["BTC", "ETH"])]
    df_final_btc_eth_final = df_final_btc_eth.groupby(
        ["year", "month", "day", "hour"], as_index=False
    ).sum()
    df_final_btc_eth_final = df_final_btc_eth_final.loc[
        df_final_btc_eth_final["market_cap"] != 0
    ]
    for i in df_final_btc_eth_final.index:
        year = df_final_btc_eth_final.loc[i, "year"]
        month = df_final_btc_eth_final.loc[i, "month"]
        day = df_final_btc_eth_final.loc[i, "day"]
        hour = df_final_btc_eth_final.loc[i, "hour"]
        df_final_btc_eth_final.loc[i, "date"] = dt.datetime(
            year, month, day, hour, 0, 0
        )

    df_final_btc_eth_final.plot(x="date", y="market_cap")
    plt.xlabel("Date", size=5)
    plt.ylabel("Marketcap", size=5)
    plt.title("OKX BTC and ETH Reserves Marketcap", size=10)

    ### total reserves busd usdt usdc m2m
    df_final_sc = df_final.loc[df_final["coin"].isin(["BUSD", "USDT", "USDC"])]
    df_final_sc = df_final_sc.groupby(
        ["year", "month", "day", "hour"], as_index=False
    ).sum()
    df_final_sc = df_final_sc.loc[df_final_sc["market_cap"] != 0]
    for i in df_final_sc.index:
        year = df_final_sc.loc[i, "year"]
        month = df_final_sc.loc[i, "month"]
        day = df_final_sc.loc[i, "day"]
        hour = df_final_sc.loc[i, "hour"]
        df_final_sc.loc[i, "date"] = dt.datetime(year, month, day, hour, 0, 0)

    df_final_sc.plot(x="date", y="market_cap")
    plt.xlabel("Date", size=5)
    plt.ylabel("Marketcap", size=5)
    plt.title("OKX USDT USDC Reserves Marketcap", size=10)
