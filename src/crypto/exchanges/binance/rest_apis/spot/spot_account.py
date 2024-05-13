"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot

spot_client_read = BinanceSpot(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

spot_client_trade = BinanceSpot(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)
