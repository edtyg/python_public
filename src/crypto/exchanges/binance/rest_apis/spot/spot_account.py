"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_READ, BINANCE_TRADE
from keys.api_work.crypto_exchanges.binance import (
    BINANCE_MCA_LTP1_READ,
    BINANCE_MCA_MAIN_READ,
)
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot

spot_client_read = BinanceSpot(
    apikey=BINANCE_READ["api_key"],
    apisecret=BINANCE_READ["api_secret"],
)

spot_client_trade = BinanceSpot(
    apikey=BINANCE_TRADE["api_key"],
    apisecret=BINANCE_TRADE["api_secret"],
)

mca_client_read = BinanceSpot(
    apikey=BINANCE_MCA_MAIN_READ["api_key"],
    apisecret=BINANCE_MCA_MAIN_READ["api_secret"],
)

mca_ltp_client_read = BinanceSpot(
    apikey=BINANCE_MCA_LTP1_READ["api_key"],
    apisecret=BINANCE_MCA_LTP1_READ["api_secret"],
)
