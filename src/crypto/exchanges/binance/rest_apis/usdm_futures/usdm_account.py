"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_usdm import BinanceUsdm

usdm_client_read = BinanceUsdm(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

usdm_client_trade = BinanceUsdm(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)
