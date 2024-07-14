"""
API Docs
https://coinmarketcap.com/api/documentation/v1/
"""

from crypto.data_providers.coinmarketcap.rest.coinmarketcap_client import CoinMarketCap
from keys.api_work.crypto_data.coinmarketcap import COINMARKETCAP

if __name__ == "__main__":
    client = CoinMarketCap(COINMARKETCAP["api_key"])

    cats = client.get_categories()
    print(cats)
