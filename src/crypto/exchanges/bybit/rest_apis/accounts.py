"""
SPOT execution program
"""

from keys.api_work.crypto_exchanges.bybit import BYBIT_KEYS
from src.crypto.exchanges.bybit.rest.bybit_client import Bybit

BYBIT_MCA_LTP1_READ = Bybit(
    api_key=BYBIT_KEYS["BYBIT_MCA_MAIN_READ"]["api_key"],
    api_secret=BYBIT_KEYS["BYBIT_MCA_MAIN_READ"]["api_secret"],
)

BYBIT_MCA_LTP1_TRADE = Bybit(
    api_key=BYBIT_KEYS["BYBIT_MCA_MAIN_TRADE"]["api_key"],
    api_secret=BYBIT_KEYS["BYBIT_MCA_MAIN_TRADE"]["api_secret"],
)
