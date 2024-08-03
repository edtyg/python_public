"""
Pulls Bybit Coin margined futures
"""

import datetime as dt

import pandas as pd
import requests

# Coin margined tickers and expiry date

# BTCUSDH24 H: First quarter; 24: 2024
# BTCUSDM24 M: Second quarter; 24: 2024
# BTCUSDU24 U: Third quarter; 24: 2024
# BTCUSDZ24 Z: Fourth quarter; 24: 2024

bybit_instruments = {
    "BTCUSDU24": dt.datetime(2024, 9, 27),
    "BTCUSDZ24": dt.datetime(2024, 12, 27),
    "ETHUSDU24": dt.datetime(2024, 9, 27),
    "ETHUSDZ24": dt.datetime(2024, 12, 27),
}


class BybitBasis:
    """simple binance class for basis calculations"""

    def __init__(self):
        self.coinm_base_endpoint = "https://api.bybit.com"
        self.timeout = 5

    def get_highest_bid_order_book(self, symbol):
        """get top of order book"""

        endpoint = "/v5/market/orderbook"
        params = {
            "category": "inverse",
            "symbol": symbol,
            "limit": 1,
        }
        response = requests.get(
            self.coinm_base_endpoint + endpoint,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        bids = data["result"]["b"][0][0]
        return bids

    def get_vol_from_klines(self, symbol):
        """get volume from klines"""

        endpoint = "/v5/market/kline"
        params = {
            "category ": "inverse",
            "symbol": symbol,
            "limit": 24,  # 24 hrs
            "interval": "60",
        }
        response = requests.get(
            self.coinm_base_endpoint + endpoint,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        taker_volume = data["result"]["list"]
        vol = 0
        for kline in taker_volume:
            vol += float(kline[5])
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
        df["contract_value"] = 1
        df["vol_usd"] = (df["vol_contracts"] * df["contract_value"]) / 1_000_000
        df["exchange"] = "Bybit"
        df = df[["instrument", "vol_usd", "price", "expiry", "exchange"]]
        return df


if __name__ == "__main__":
    bybit_client = BybitBasis()
    bybit_df = bybit_client.get_list_highest_bids(dict_of_instruments)
    print(bybit_df)
