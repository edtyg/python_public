"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_cross_margin import BinanceCrossMargin
from src.crypto.exchanges.binance.rest.binance_isolated_margin import (
    BinanceIsolatedMargin,
)

xmargin_client_read = BinanceCrossMargin(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

xmargin_client_trade = BinanceCrossMargin(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)


imargin_client_read = BinanceIsolatedMargin(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

imargin_client_trade = BinanceIsolatedMargin(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)
