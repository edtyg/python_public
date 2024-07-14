"""
order params for LIMIT PRICE TWAP
placing TWAP orders but with a limit price
note that quote quantity cannot be specified for limit orders
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_TRADE
from keys.api_work.crypto_exchanges.binance import BINANCE_MCA_LTP1_TRADE

SPREAD_PARAMS = {
    "spot_base_ticker": "ETH",  # base ticker
    "spot_quote_ticker": "USDT",  # quote ticker
    "spot_ticker": "ETHUSDT",  # base + quote ticker
    "futures_ticker": "ETHUSD_240927",
    "spread_direction": "sell",  # sell = sell futures, buy spot and vice versa
    "total_trade_size": 15,  # trade size in USDT terms
    "clip_size_type": "quote",  # trade size in base or quote currency
    "contract_clip_size": 1,  # number of contracts per clip
    "time_interval_seconds": 10,  # execution time interval
    "client_order_id": "31_05_2024_eth_spread",  # orderid
    "tg_chatgrp": 6,  # chatgroup 1 to 5
}

TRADING_ACCOUNT = BINANCE_TRADE
