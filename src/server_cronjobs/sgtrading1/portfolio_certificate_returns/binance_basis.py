"""
Pulls Binance Coin margined futures
"""

import datetime as dt

import pandas as pd
import requests

# Coin margined tickers and expiry date
binance_instruments = {
    "BTCUSD_240927": dt.datetime(2024, 9, 27),
    "BTCUSD_241227": dt.datetime(2024, 12, 27),
    "ETHUSD_240927": dt.datetime(2024, 9, 27),
    "ETHUSD_241227": dt.datetime(2024, 12, 27),
}


class BinanceBasis:
    """simple binance class for basis calculations"""

    def __init__(self):
        self.coinm_base_endpoint = "https://dapi.binance.com"
        self.timeout = 5

    def get_highest_bid_order_book(self, symbol):
        """get top of order book"""
        endpoint = "/dapi/v1/depth"
        params = {"symbol": symbol, "limit": 5}
        response = requests.get(
            self.coinm_base_endpoint + endpoint,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        bids = data["bids"][0][0]
        return bids

    def get_vol_from_klines(self, symbol):
        """get volume from klines"""
        endpoint = "/dapi/v1/klines"
        params = {
            "symbol": symbol,
            "interval": "1h",
            "limit": 24,  # 24 hours
        }
        response = requests.get(
            self.coinm_base_endpoint + endpoint,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        df = pd.DataFrame(data)
        vol = df.iloc[:, 5].astype(float).sum()  # 24 hour number of contracts
        return vol

    def get_list_highest_bids(self, dict_of_instruments: dict):
        """get highest bids"""
        instrument = []
        price = []
        expiry = []
        vol = []
        for i in dict_of_instruments:
            price_i = self.get_highest_bid_order_book(i)

            instrument.append(i)
            vol.append(self.get_vol_from_klines(i))  # get volume in contracts
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
        df["exchange"] = "Binance"
        df = df[["instrument", "vol_usd", "price", "expiry", "exchange"]]
        return df


if __name__ == "__main__":
    binance_client = BinanceBasis()
    binance_df = binance_client.get_list_highest_bids(dict_of_instruments)
    print(binance_df)
