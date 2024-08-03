"""
deribit accounts
"""

from keys.api_personal.crypto_exchanges.deribit import DERIBIT_READ, DERIBIT_TRADE
from src.crypto.exchanges.deribit.rest.deribit_client import DeribitRest

deribit_read = DeribitRest(
    apikey=DERIBIT_READ["api_key"],
    apisecret=DERIBIT_READ["api_secret"],
)

deribit_trade = DeribitRest(
    apikey=DERIBIT_TRADE["api_key"],
    apisecret=DERIBIT_TRADE["api_secret"],
)
