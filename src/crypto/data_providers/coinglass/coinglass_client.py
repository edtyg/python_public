"""
https://coinglass.readme.io/reference/getting-started-with-your-api
API Docs for coinglass - futures and options data
"""

import requests

from local_credentials.api_personal.crypto_blockchain.coinglass import COINGLASS


class CoinGlass:
    """rest api for coin glass"""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.url = "https://open-api.coinglass.com/public"
        self.headers = {"coinglassSecret": self.apikey}
        self.timeout = 10

    ###############
    ### Futures ###
    ###############

    def get_open_interest(self, params: dict) -> dict:
        """Open Interest
        https://coinglass.readme.io/reference/open-interest

        Args:
            param       default     desc
            symbol      str         Symbol
        """
        endpoint = "/v2/open_interest"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    ###############
    ### Options ###
    ###############

    def get_option(self, params: dict) -> dict:
        """Gets Option data

        https://coinglass.readme.io/reference/option

        Args:
            param       default     desc
            symbol      str         Symbol
        """
        endpoint = "/v2/option"
        response = requests.get(
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = CoinGlass(COINGLASS["api_key"])

    futures_interest = client.get_open_interest({"symbol": "BTC"})
    print(futures_interest)

    option = client.get_option({"symbol": "BTC"})
    print(option)
