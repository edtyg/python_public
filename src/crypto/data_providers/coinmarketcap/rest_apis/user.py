"""
Coinmarketcap user - paid version
"""

from crypto.data_providers.coinmarketcap.rest.coinmarketcap_client import CoinMarketCap
from keys.api_work.crypto_data.coinmarketcap import COINMARKETCAP

cmc_user = CoinMarketCap(
    apikey=COINMARKETCAP["api_key"],
)
