"""
pip install ccxt
cryptocurrency library
"""

import ccxt
import pandas as pd

# print(ccxt.exchanges)

binance = ccxt.binance()

market_binance = binance.load_markets()
df_market_binance = pd.DataFrame(market_binance)

ticker_binance = binance.fetch_ticker("BTC/USDT")
print(ticker_binance)
