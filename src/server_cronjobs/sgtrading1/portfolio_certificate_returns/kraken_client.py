# API Docs Here
# https://coinmarketcap.com/api/documentation/v1/
# Current API KEY - Startup Subscription

from requests import request
from typing import Optional, Dict
import pandas as pd
import datetime as dt


class kraken:
    def __init__(self):
        self.url = "https://api.kraken.com/0"

    def get_ohlc(self, params: dict):
        """kraken ohlc data

        Args:
            params (params: dict): parameters for api call - required

        params      type        Description
        pair        string      'XBTUSD', 'ETHUSD'
        interval    integer     1, 5, 15 etc... time frame interval in minutes
        """

        endpoint = "/public/OHLC"
        response = request("GET", self.url + endpoint, params=params)
        response_data = response.json()
        symbol = list(response_data["result"].keys())[0]
        data = response_data["result"][symbol]

        columns = ["ts", "open", "high", "low", "close", "vwap", "volume", "count"]
        df = pd.DataFrame(data, columns=columns)
        df["date"] = pd.to_datetime(df["ts"], unit="s")

        last_row = df.tail(24)
        return last_row


if __name__ == "__main__":
    client = kraken()

    btc_data = client.get_ohlc(params={"pair": "XBTUSD", "interval": 60})
    print(btc_data)
    eth_data = client.get_ohlc(params={"pair": "ETHUSD", "interval": 60})
    print(eth_data)
