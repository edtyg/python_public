"""
Wallet transfers
"""

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_trade


def make_transfer(client):
    """Makes transfers within accounts

    Args:
        client (_type_): binance spot client
    """
    transfer = client.post_user_universal_transfer(
        {
            "type": "ISOLATED_MARGIN_MAIN",
            "asset": "USDT",
            "amount": 0.01,
            "fromSymbol": "BTCUSDT",
        }
    )
    return transfer


if __name__ == "__main__":

    transfer1 = make_transfer(spot_client_trade)
    print(transfer1)
