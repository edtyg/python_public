"""
SPOT execution program
"""

from keys.api_work.crypto_exchanges.bybit import (
    BYBIT_MCA_LTP1_READ,
    BYBIT_MCA_LTP1_TRADE,
)
from src.crypto.exchanges.bybit.rest.bybit_client import Bybit

spot_client_read = Bybit(
    apikey=BYBIT_MCA_LTP1_READ["api_key"],
    apisecret=BYBIT_MCA_LTP1_READ["api_secret"],
)

spot_client_trade = Bybit(
    apikey=BYBIT_MCA_LTP1_TRADE["api_key"],
    apisecret=BYBIT_MCA_LTP1_TRADE["api_secret"],
)
