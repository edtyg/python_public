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
            "type": "MAIN_UMFUTURE",
            "asset": "BTC",
            "amount": 0.01,
        }
    )
    return transfer


if __name__ == "__main__":

    transfer1 = make_transfer(spot_client_trade)
    print(transfer1)
