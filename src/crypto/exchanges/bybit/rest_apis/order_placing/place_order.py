"""
Bybit Spot Account balances
"""

import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_TRADE
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


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
            "symbol": "ETHUSDT",
            "side": "buy",
            "orderType": "Market",
            "qty": "4.51613",
            "marketUnit": "quoteCoin",  # only for market orders
            "orderLinkId": "test_1709262829",
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
            "symbol": "ETHUSDT",
            "orderId": "1629702872117808128",
            "qty": "0.04",
            "price": "3000",
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
    account = BYBIT_MCA_MAIN_TRADE
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    order1 = place_order(client)
    print(order1)

    # amend_order1 = amend_order(client)
    # print(amend_order1)

    # cancel_order1 = cancel_order(client)
    # print(cancel_order1)
