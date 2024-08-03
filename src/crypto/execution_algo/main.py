"""
Execution Algo
"""

import datetime as dt
import sys

from keys.api_work.crypto_exchanges.binance import BINANCE_KEYS
from keys.api_work.crypto_exchanges.bybit import BYBIT_KEYS
from keys.api_work.crypto_exchanges.okx import OKX_KEYS
from src.crypto.execution_algo.binance.binance_algo import BinanceAlgoTrading
from src.crypto.execution_algo.bybit.bybit_algo import BybitAlgoTrading
from src.crypto.execution_algo.okx.okx_algo import OkxAlgoTrading
from src.libraries.configparser.config_setter import ConfigSetter

if __name__ == "__main__":
    # config_path = sys.argv[1]
    # log_path = sys.argv[2] + dt.datetime.now().strftime("%Y-%m-%d") + "-"
    # mode = sys.argv[3]
    # trading_params = sys.argv[4]

    CONFIG_PATH = "C:/Users/EdgarTan/Documents/Github/python/config/trade_execution_algos/algo_trading_params.ini"
    LOG_PATH = f"C:/Users/EdgarTan/Documents/Github/python/logs/trade_execution_algos/trade_executions/{dt.datetime.now().strftime('%Y-%m-%d')}-"
    TICKER = "btcusdt-params"

    CONFIG = ConfigSetter(CONFIG_PATH)
    TRADING_PARAMS = CONFIG.get_section_data(TICKER)

    if TRADING_PARAMS["exchange"].upper() == "BINANCE":
        client = BinanceAlgoTrading(
            api_key=BINANCE_KEYS[TRADING_PARAMS["account_name"]]["api_key"],
            api_secret=BINANCE_KEYS[TRADING_PARAMS["account_name"]]["api_secret"],
            file_path=LOG_PATH,
            file_name="Binance.log",
            save_mode="a",
        )
        client.binance_trading_algo(TRADING_PARAMS)
    elif TRADING_PARAMS["exchange"].upper() == "OKX":
        client = OkxAlgoTrading(
            api_key=OKX_KEYS[TRADING_PARAMS["account_name"]]["api_key"],
            api_secret=OKX_KEYS[TRADING_PARAMS["account_name"]]["api_secret"],
            file_path=LOG_PATH,
            file_name="Okx.log",
            save_mode="a",
            passphrase=OKX_KEYS[TRADING_PARAMS["account_name"]]["passphrase"],
        )
        client.okx_trading_algo(TRADING_PARAMS)
    elif TRADING_PARAMS["exchange"].upper() == "BYBIT":
        client = BybitAlgoTrading(
            api_key=BYBIT_KEYS[TRADING_PARAMS["account_name"]]["api_key"],
            api_secret=BYBIT_KEYS[TRADING_PARAMS["account_name"]]["api_secret"],
            file_path=LOG_PATH,
            file_name="Bybit.log",
            save_mode="a",
        )
        client.bybit_trading_algo(TRADING_PARAMS)
