"""
Script to Pull USD margined Perp Funding rates 
Binance, Bybit, OKX
"""

# import asyncio
import os

import pandas as pd

from src.utils.utils import Utils


def okx_rates():
    """
    async get usdm funding rates
    """

    # get okx futures instruments
    okx_instruments = Utils.get_request(
        base_url="https://www.okx.com/",
        endpoint="api/v5/public/instruments",
        headers=None,
        params={"instType": "SWAP"},
    )["data"]
    df_okx_instruments = pd.DataFrame(okx_instruments)
    df_okx_instruments = df_okx_instruments.loc[
        (
            (df_okx_instruments["ctType"] == "linear")
            & (df_okx_instruments["settleCcy"] == "USDT")
        )
    ]
    instrument_id = df_okx_instruments["instId"]
    # instrument_id = instrument_id[:5]
    # get volume and average funding
    data = {}

    # get historical funding rates
    df_final = pd.DataFrame()
    volume_threshold = 1
    print(f"volume threshold set at {volume_threshold}")
    for inst in instrument_id:
        # gets contract traded volumes first
        taker_volume = Utils.get_request(
            base_url="https://www.okx.com/",
            endpoint="api/v5/rubik/stat/taker-volume-contract",
            headers=None,
            params={"instId": inst, "period": "1D", "limit": 1, "unit": 2},
        )
        daily_usd_volume = float(taker_volume["data"][0][1]) + float(
            taker_volume["data"][0][2]
        )

        # funding rate history
        print(f"daily USDT volume of {inst} = {daily_usd_volume}")
        if daily_usd_volume >= volume_threshold:
            funding_rate = Utils.get_request(
                base_url="https://www.okx.com/",
                endpoint="api/v5/public/funding-rate-history",
                headers=None,
                params={"instId": inst, "limit": 100},
            )["data"]
            df_funding_rate = pd.DataFrame(funding_rate)
            df_funding_rate["datetime"] = pd.to_datetime(
                df_funding_rate["fundingTime"], unit="ms"
            )
            df_funding_rate.set_index("datetime", inplace=True)
            df_funding_rate = df_funding_rate[["realizedRate"]]
            average_funding_rate = (
                df_funding_rate["realizedRate"].astype("float").mean()
            )
            df_funding_rate.rename(columns={"realizedRate": inst}, inplace=True)

            if df_final.empty:
                df_final = df_funding_rate
            else:
                df_final = pd.merge(
                    df_final,
                    df_funding_rate,
                    left_index=True,
                    right_index=True,
                    how="left",
                )

            print(df_funding_rate)
            data[inst] = [daily_usd_volume, average_funding_rate]
        else:
            continue

    df_summary = pd.DataFrame(data).T
    df_summary.columns = ["daily_volume", "average_8hr_funding_rate"]
    print(df_summary)
    print(df_final)

    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    output_excel = "okx_usdm_funding_rates.xlsx"
    writer = pd.ExcelWriter(save_path + output_excel)  # writer for xlsx files

    df_final.to_excel(writer, sheet_name="okx_usdm_funding")
    df_summary.to_excel(writer, sheet_name="okx_summary")
    writer.close()
    print("file Saved")


def bybit_rates():
    """
    get usdm funding rates
    """

    # get okx futures instruments
    bybit_instruments = Utils.get_request(
        base_url="https://api.bybit.com/",
        endpoint="v5/market/instruments-info",
        headers=None,
        params={"category": "linear"},
    )["result"]["list"]
    df_bybit_instruments = pd.DataFrame(bybit_instruments)
    df_bybit_instruments = df_bybit_instruments.loc[
        (
            (df_bybit_instruments["quoteCoin"] == "USDT")
            & (df_bybit_instruments["settleCoin"] == "USDT")
        )
    ]
    instrument_id = df_bybit_instruments["symbol"]
    # instrument_id = instrument_id[:1]
    print(instrument_id)

    # get volume and average funding
    data = {}

    # get historical funding rates
    df_final = pd.DataFrame()
    volume_threshold = 1
    print(f"volume threshold set at {volume_threshold}")
    for inst in instrument_id:
        # gets contract traded volumes first
        taker_volume = Utils.get_request(
            base_url="https://api.bybit.com/",
            endpoint="v5/market/kline",
            headers=None,
            params={
                "category ": "linear",
                "symbol": inst,
                "limit": 24,
                "interval": "60",
            },
        )
        taker_volume = taker_volume["result"]["list"]
        daily_usd_volume = 0
        for kline in taker_volume:
            daily_usd_volume += float(kline[6])

        # funding rate history
        print(f"daily USDT volume of {inst} = {daily_usd_volume}")
        if daily_usd_volume >= volume_threshold:
            funding_rate = Utils.get_request(
                base_url="https://api.bybit.com/",
                endpoint="v5/market/funding/history",
                headers=None,
                params={"category": "linear", "symbol": inst, "limit": 200},
            )["result"]["list"]
            df_funding_rate = pd.DataFrame(funding_rate)
            df_funding_rate["datetime"] = pd.to_datetime(
                df_funding_rate["fundingRateTimestamp"], unit="ms"
            )
            df_funding_rate.set_index("datetime", inplace=True)
            df_funding_rate = df_funding_rate[["fundingRate"]]
            average_funding_rate = df_funding_rate["fundingRate"].astype("float").mean()
            df_funding_rate.rename(columns={"fundingRate": inst}, inplace=True)
            if df_final.empty:
                df_final = df_funding_rate
            else:
                df_final = pd.merge(
                    df_final,
                    df_funding_rate,
                    left_index=True,
                    right_index=True,
                    how="left",
                )

            print(df_funding_rate)
            data[inst] = [daily_usd_volume, average_funding_rate]
        else:
            continue

    df_summary = pd.DataFrame(data).T
    df_summary.columns = ["daily_volume", "average_8hr_funding_rate"]
    print(df_summary)
    print(df_final)

    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    output_excel = "bybit_usdm_funding_rates.xlsx.xlsx"
    writer = pd.ExcelWriter(save_path + output_excel)  # writer for xlsx files

    df_final.to_excel(writer, sheet_name="bybit_usdm_funding")
    df_summary.to_excel(writer, sheet_name="bybit_summary")
    writer.close()
    print("file Saved")


if __name__ == "__main__":
    # okx_rates()
    bybit_rates()
