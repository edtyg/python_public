"""
Coinmarketcap user - paid version
"""

from local_credentials.api_work.crypto_data.coinmarketcap import COINMARKETCAP
from python.crypto.data_providers.coinmarketcap.rest.coinmarketcap_client import (
    CoinMarketCap,
)

cmc_user = CoinMarketCap(
    apikey=COINMARKETCAP["api_key"],
)
