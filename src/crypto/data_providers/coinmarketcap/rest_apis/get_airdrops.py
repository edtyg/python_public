"""
API Docs
https://coinmarketcap.com/api/documentation/v1/
"""

from local_credentials.api_work.crypto_data.coinmarketcap import COINMARKETCAP
from python.crypto.data_providers.coinmarketcap.rest.coinmarketcap_client import (
    CoinMarketCap,
)

if __name__ == "__main__":
    client = CoinMarketCap(COINMARKETCAP["api_key"])

    airdrop = client.get_airdrops()
    print(airdrop)
