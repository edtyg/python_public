"""
Alphavantage API - free key
https://www.alphavantage.co/documentation/#
"""
import requests
from local_credentials.api_key_data import ALPHAVANTAGE_KEY_1


class AlphaVantage:
    """Alphavantage rest api"""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.url = "https://www.alphavantage.co/query"
        self.timeout = 5

    ##############
    ### Crypto ###
    ##############

    def get_crypto_ccy_rate(self, params: dict):
        """
        gets crypto currency rate

        params:
            params          required    eg
            function        yes         CURRENCY_EXCHANGE_RATE
            from_currency   yes         BTC
            to_currency     yes         USD
            apikey          yes         apikey
        """

        response = requests.request(
            "GET", self.url, params=params, timeout=self.timeout
        )
        data = response.json()

        return data


if __name__ == "__main__":
    client = AlphaVantage(ALPHAVANTAGE_KEY_1)

    rate = client.get_crypto_ccy_rate(
        {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": "BTC",
            "to_currency": "USD",
            "apikey": client.apikey,
        }
    )
