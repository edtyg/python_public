"""
Coin Margined APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""
from typing import Dict, Optional

import requests
from binance_client import Binance
from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET


class BinanceCoinm(Binance):
    """
    CoinMargined APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)

        self.coinm_url = "https://dapi.binance.com"
        self.timeout = 5

    #####################
    ### coinm methods ###
    #####################

    def get_coinm_acc_balance(self) -> dict:
        """
        Signed Request -> gets your USD Margined Futures Account balance

        No Params needed for this api call

        Returns:
            dict: [response from api call]
        """

        url = self.signed_request_url(self.coinm_url, "/dapi/v1/account")
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()

        return data

    def get_coinm_ticker_price(self, params: Optional[Dict] = None) -> dict:
        """
        Public request, no signature required

         Args:
            params (dict, optional):
                    'symbol' = 'BTCUSDT' -> str (optional parameter)

            If the symbol is not sent, prices for all symbols will be returned in an array.

        Returns:
            dict: [response from api call]
        """

        url = self.signed_request_url(self.coinm_url, "/dapi/v1/ticker/price", params)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()

        return data


if __name__ == "__main__":
    client = BinanceCoinm(BINANCE_KEY, BINANCE_SECRET)

    balance = client.get_coinm_acc_balance()
    print(balance)

    ticker = client.get_coinm_ticker_price()
    print(ticker)
