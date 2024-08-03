"""
client to pull deribit coin margined futures tickers
"""

import datetime as dt

import pandas as pd
import requests

deribit_instruments = {
    "BTC-27SEP24": dt.datetime(2024, 9, 27),
    "BTC-27DEC24": dt.datetime(2024, 12, 27),
    "ETH-27SEP24": dt.datetime(2024, 9, 27),
    "ETH-27DEC24": dt.datetime(2024, 12, 27),
}


class DeribitBasis:
    """simple deribit class for basis calculations"""

    def __init__(self):
        self.endpoint = "https://www.deribit.com/api/v2"
        self.timeout = 5

    def get_instruments_list(self, instrument):
        """'BTC, 'ETH' or 'USDT' for instrument"""
        endpoint = "/public/get_instruments"
        params = {"currency": instrument}
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        data = response.json()["result"]

        non_options_data = []
        for i in data:
            # exclude options tickers
            if i["instrument_name"].endswith("C") or i["instrument_name"].endswith("P"):
                next
            else:
                non_options_data.append(i["instrument_name"])
        return non_options_data

    def get_highest_bid_order_book(self, instrument):
        """gets top of order book"""
        endpoint = "/public/get_order_book"
        params = {"instrument_name": instrument}
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        order_book = response.json()["result"]
        bids = order_book["bids"][0][0]
        print(bids)
        return bids

    def get_ticker(self, symbol):
        """gets ticker"""
        endpoint = "/public/ticker"
        params = {
            "instrument_name": symbol,
        }
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        data = response.json()["result"]["stats"]["volume_usd"] / 1000000
        return data

    def get_list_highest_bids(self, dict_of_instruments):
        """gets list of highest bids"""
        instrument = []
        price = []
        expiry = []
        vol = []

        for i in dict_of_instruments:
            price_i = self.get_highest_bid_order_book(i)

            instrument.append(i)
            vol.append(self.get_ticker(i))  # get volume
            price.append(price_i)
            expiry.append(dict_of_instruments[i])

        df = pd.DataFrame(
            {"instrument": instrument, "vol_usd": vol, "price": price, "expiry": expiry}
        )
        df["exchange"] = "Deribit"
        return df


if __name__ == "__main__":
    deribit_client = DeribitBasis()
    deribit_df = deribit_client.get_list_highest_bids(dict_of_instruments)
    print(deribit_df)
