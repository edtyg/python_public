"""
Bybit Spot Account balances
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.bybit import BYBIT_KEYS
from src.crypto.exchanges.bybit.rest.bybit_client import Bybit


def place_order(client):
    """Places an order

    Args:
        client (_type_): bybit spot client

    Returns:
    Order Response
    {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1630516916663880704', 'orderLinkId': '1630516916663880705'}, 'retExtInfo': {}, 'time': 1709108763237}
    {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '1630517627095092226', 'orderLinkId': '1630517627095092227'}, 'retExtInfo': {}, 'time': 1709108847927}
    """
    order = client.place_order(
        {
            "category": "spot",
            "symbol": "BTCUSDT",
            "isLeverage": "1",
            "side": "sell",
            "orderType": "Limit",
            "qty": "0.0004",
            "price": "70001.1",
            "timeInForce": "IOC",
        }
    )
    return order


def amend_order(client):
    """Amend orders

    Args:
        client (_type_): bybit spot client
    """
    amend_spot_order = client.amend_order(
        {
            "category": "spot",
            "symbol": "BTCUSDT",
            "isLeverage": "1",
            "side": "sell",
            "orderType": "Limit",
            "timeInForce": "IOC",
            "price": "70001.26",
            "qty": 0.0005,
        }
    )
    return amend_spot_order


def cancel_order(client):
    """
    Cancel Order
    """
    cancel_spot_order = client.cancel_order(
        {
            "category": "spot",
            "symbol": "ETHUSDT",
            "orderId": "1629702872117808128",
        }
    )
    return cancel_spot_order


if __name__ == "__main__":
    account = BYBIT_KEYS["BYBIT_MCA_LTP1_TRADE"]
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    order1 = place_order(client)
    print(order1)
    order_id = order1["result"]["orderId"]

    import time

    time.sleep(1)
    order_history = client.get_order_history(
        {
            "category": "spot",
            "symbol": "BTCUSDT",
            "orderId": order_id,
        }
    )
    print(order_history)

    # amend_order1 = amend_order(client)
    # print(amend_order1)

    # cancel_order1 = cancel_order(client)
    # print(cancel_order1)
