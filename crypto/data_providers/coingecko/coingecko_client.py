"""
API Docs Here
https://www.coingecko.com/en/api/documentation
no api key for free version
"""

from typing import Optional

from requests import request


class CoinGecko:
    """coingecko rest api"""

    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3"
        self.timeout = 5

    def get_coins_list(self, params: Optional[dict] = None):
        """Gets list of all support coin id, name and symbol from coingecko"""

        endpoint = "/coins/list"
        response = request(
            "GET", self.url + endpoint, params=params, timeout=self.timeout
        )

        data = response.json()

        return data

    def get_coins_markets(self, params: Optional[dict] = None):
        """

        Args:
            params (dict): parameters for api call

        params          type        desc
        vs_currency     string      usd, eur, jpy etc (quote currency)
        ids             string      comma separated
        """

        endpoint = "/coins/markets"
        response = request(
            "GET", self.url + endpoint, params=params, timeout=self.timeout
        )

        data = response.json()

        return data

    def get_coin_market_chart_range(self, coin_id, params: Optional[dict] = None):
        """

        Args:
            params (dict): parameters for api call

        params          type        desc
        vs_currency     string      usd, eur, jpy etc (quote currency)
        from            string      timestamp
        to              string      timestamp
        """

        endpoint = f"/coins/{coin_id}/market_chart/range"
        response = request(
            "GET", self.url + endpoint, params=params, timeout=self.timeout
        )

        data = response.json()

        return data


if __name__ == "__main__":
    client = CoinGecko()
    coin_list = client.get_coins_list()
    print(coin_list)
