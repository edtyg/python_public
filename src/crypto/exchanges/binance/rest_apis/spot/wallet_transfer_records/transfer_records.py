"""
Get wallet transfer records
"""

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_trade


def get_wallet_transfers(client):
    """

    Args:
        client (_type_): binance spot client
    """
    transfer_record = client.get_user_universal_transfer(
        {
            "type": "MAIN_UMFUTURE",
        }
    )
    return transfer_record


if __name__ == "__main__":

    df = get_wallet_transfers(spot_client_trade)
    print(df)
