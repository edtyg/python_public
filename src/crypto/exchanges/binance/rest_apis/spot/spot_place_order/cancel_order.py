"""
SPOT execution program
"""

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_trade


def cancel_spot_rder(client):
    """
    Cancels spot order

    Args:
        client (_type_): binance spot client
    """
    order_params = {
        "symbol": "NEARUSDT",
        "orderId": "2631762199",
    }

    order = client.delete_order(order_params)
    return order


if __name__ == "__main__":

    order1 = cancel_spot_rder(spot_client_trade)
    print(order1)
