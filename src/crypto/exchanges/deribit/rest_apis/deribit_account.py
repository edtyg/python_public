"""
deribit accounts
"""

from keys.api_personal.crypto_exchanges.deribit import DERIBIT_READ, DERIBIT_TRADE
from src.crypto.exchanges.deribit.rest.deribit_client import DeribitRestClient

deribit_read = DeribitRestClient(
    apikey=DERIBIT_READ["api_key"],
    apisecret=DERIBIT_READ["api_secret"],
)

deribit_trade = DeribitRestClient(
    apikey=DERIBIT_TRADE["api_key"],
    apisecret=DERIBIT_TRADE["api_secret"],
)
