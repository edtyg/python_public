"""
SPOT execution program
"""

from keys.api_personal.crypto_exchanges.binance import BINANCE_TRADE
from src.crypto.exchanges.binance.rest.binance_isolated_margin import (
    BinanceIsolatedMargin,
)


def place_isolated_margin_order(client):
    """Places isolated margin order"""
    order = client.post_margin_new_order(
        {
            "symbol": "BTCUSDT",
            "isIsolated": True,
            "side": "SELL",
            "type": "LIMIT",
            "quantity": 0.001,
            "price": 55000,
            "timeInForce": "GTC",
        }
    )
    return order


def delete_isolated_margin_order(client):
    """deletes a isolated margin order"""
    delete_order = client.delete_margin_cancel_order(
        {
            "symbol": "BTCUSDT",
            "isIsolated": True,
            "side": "SELL",
            "orderId": 24633353528,
            # "clientOrderId": ,
        }
    )
    return delete_order


if __name__ == "__main__":
    api = BINANCE_TRADE
    binance_cross_margin_client = BinanceIsolatedMargin(
        api["api_key"],
        api["api_secret"],
    )

    # order = place_isolated_margin_order(binance_cross_margin_client)
    # print(order)

    # delete_order = delete_isolated_margin_order(binance_cross_margin_client)
    # print(delete_order)
