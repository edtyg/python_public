# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:31:24 2024

@author: Edgar Tan
"""

from src.crypto.exchanges.binance.rest_apis.coinm_futures.coinm_account import (
    coinm_client_trade,
)

order_params = {"symbol": "BTCUSD_240628", "orderId": "1716432265"}

order = coinm_client_trade.get_query_order(order_params)
print(order)
