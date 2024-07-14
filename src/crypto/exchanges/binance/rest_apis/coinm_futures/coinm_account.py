"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_coinm import BinanceCoinm

coinm_client_read = BinanceCoinm(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

coinm_client_trade = BinanceCoinm(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)
