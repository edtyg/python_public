"""
API Docs
https://coinmarketcap.com/api/documentation/v1/
"""
from typing import Dict, Optional

from requests import request

from local_credentials.api_key_data import COINMARKETCAP_KEY_FREE


class CoinMarketCap:
    """coinmarketcap rest api"""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.url = "https://pro-api.coinmarketcap.com"
        self.headers = {"X-CMC_PRO_API_KEY": self.apikey}
        self.timeout = 10

    def get_listings_latest(self, params: Optional[Dict] = None):
        """get Listings Latest
        https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest

        Args:
            params (Optional[Dict], optional): parameters for api call. Defaults to {}.

        params  type        Description
        """
        endpoint = "/v1/cryptocurrency/listings/latest"
        response = request(
            "GET",
            self.url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = CoinMarketCap(COINMARKETCAP_KEY_FREE)
    listings = client.get_listings_latest()
    print(listings)
