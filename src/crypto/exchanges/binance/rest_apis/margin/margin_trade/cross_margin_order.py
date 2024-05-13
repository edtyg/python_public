"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_cross_margin import BinanceCrossMargin


def place_cross_margin_order(client):
    """Places cross margin order"""
    order = client.post_margin_new_order(
        {
            "symbol": "BTCUSDT",
            "isIsolated": False,
            "side": "BUY",
            "type": "LIMIT",
            "quantity": 0.001,
            "price": 15000,
            "timeInForce": "GTC",
        }
    )
    return order


def delete_cross_margin_order(client):
    """deletes a cross margin order"""
    delete_order = client.delete_margin_cancel_order(
        {
            "symbol": "BTCUSDT",
            "isIsolated": False,
            "side": "BUY",
            "orderId": 24632809098,
            # "clientOrderId": ,
        }
    )
    return delete_order


if __name__ == "__main__":
    api = BINANCE_TRADE
    binance_cross_margin_client = BinanceCrossMargin(
        api["api_key"],
        api["api_secret"],
    )

    # order = place_cross_margin_order(binance_cross_margin_client)
    # print(order)

    # delete_order = delete_cross_margin_order(binance_cross_margin_client)
    # print(delete_order)
