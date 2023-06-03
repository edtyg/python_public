"""
API docs here for DYDX - defi perpertual futures trading platform
https://docs.dydx.exchange/#terms-of-service-and-privacy-policy
"""

import requests

from local_credentials.api_key_defi import DYDX_KEY, DYDX_SECRET, DYDX_PASSPHRASE


class DYDX:
    """rest api for DYDX"""

    def __init__(self, apikey: str, apisecret: str, passphrase: str) -> None:
        self.apikey = apikey
        self.apisecret = apisecret
        self.passphrase = passphrase
        self.base_url = "https://api.dydx.exchange"
        self.timeout = 10

    #######################
    ### public http api ###
    #######################

    def get_markets(self) -> dict:
        """gets all dydx markets
        https://dydxprotocol.github.io/v3-teacher/#get-markets
        """
        endpoint = "/v3/markets"
        response = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return response.json()

    def get_orderbook(self, market: str) -> dict:
        """gets orderbook
        https://dydxprotocol.github.io/v3-teacher/#get-orderbook
        """
        endpoint = f"/v3/orderbook/{market}"
        response = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return response.json()

    def get_trades(self, market: str) -> dict:
        """get trades
        https://dydxprotocol.github.io/v3-teacher/#get-trades
        """
        endpoint = f"/v3/trades/{market}"
        response = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return response.json()

    def get_market_stats(self, market: str) -> dict:
        """get market stats
        https://dydxprotocol.github.io/v3-teacher/#get-market-stats
        """
        endpoint = f"/v3/stats/{market}"
        response = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return response.json()


if __name__ == "__main__":
    client = DYDX(DYDX_KEY, DYDX_SECRET, DYDX_PASSPHRASE)

    MARKET_TICKER = "ETH-USD"

    markets = client.get_markets()
    ob = client.get_orderbook(MARKET_TICKER)
    trades = client.get_trades(MARKET_TICKER)
    market_stats = client.get_market_stats(MARKET_TICKER)
