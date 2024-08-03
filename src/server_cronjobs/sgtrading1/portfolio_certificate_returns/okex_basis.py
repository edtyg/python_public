"""
client to pull okx coin margined futures tickers
"""

import datetime as dt

import pandas as pd
import requests

okx_instruments = {
    "BTC-USD-240927": dt.datetime(2024, 9, 27),
    "BTC-USD-241227": dt.datetime(2024, 12, 27),
    "ETH-USD-240927": dt.datetime(2024, 9, 27),
    "ETH-USD-241227": dt.datetime(2024, 12, 27),
}


class OkxBasis:
    """simple okx class for basis calculations"""

    def __init__(self):
        self.endpoint = "https://www.okx.com"
        self.timeout = 5

    def get_instruments_list(self):
        """gets list of tradeable instruments"""
        endpoint = "/api/v5/public/instruments"
        params = {"instType": "FUTURES"}
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        data = response.json()["data"]
        empty = []
        for i in data:
            empty.append(i["instId"])
        return empty

    def get_highest_bid_order_book(self, symbol):
        """gets top of orderbook"""
        endpoint = "/api/v5/market/books"
        params = {"instId": symbol}
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        data = response.json()["data"][0]
        bids = data["bids"][0][0]
        return bids

    def get_candles(self, symbol):
        """gets ohlcv candles"""
        endpoint = "/api/v5/market/candles"
        params = {"instId": symbol, "bar": "1H", "limit": "24"}
        response = requests.get(
            self.endpoint + endpoint, params=params, timeout=self.timeout
        )
        data = response.json()["data"]
        df = pd.DataFrame(data)
        vol = df.iloc[:, 5].astype(float).sum()
        return vol

    def get_list_highest_bids(self, dict_of_instruments):
        """gets highest bids"""
        instrument = []
        price = []
        expiry = []
        vol = []

        for i in dict_of_instruments:
            price_i = self.get_highest_bid_order_book(i)

            instrument.append(i)
            vol.append(self.get_candles(i))  # get volume
            price.append(price_i)
            expiry.append(dict_of_instruments[i])

        df = pd.DataFrame(
            {
                "instrument": instrument,
                "vol_contracts": vol,
                "price": price,
                "expiry": expiry,
            }
        )
        df["contract_value"] = [
            100 if x.startswith("BTC") else 10 for x in df["instrument"]
        ]
        df["vol_usd"] = (df["vol_contracts"] * df["contract_value"]) / 1000000
        df["exchange"] = "Okex"
        df = df[["instrument", "vol_usd", "price", "expiry", "exchange"]]
        return df


if __name__ == "__main__":
    okex_client = OkxBasis()
    okex_df = okex_client.get_list_highest_bids(dict_of_instruments)
    print(okex_df)
