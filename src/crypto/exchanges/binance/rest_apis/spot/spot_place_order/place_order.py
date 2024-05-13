"""
SPOT execution program
"""

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_trade


def place_spot_order(client):
    """
    Places spot order

    Args:
        client (_type_): binance spot client
    """
    order_params = {
        "symbol": "NEARUSDT",
        "side": "sell",
        "type": "LIMIT",
        "quantity": 10,
        "price": 10,
        "timeInForce": "GTC",
    }

    order = client.post_order(order_params)
    return order


if __name__ == "__main__":

    order1 = place_spot_order(spot_client_trade)
    print(order1)
