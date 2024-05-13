"""
Address
"""

from src.crypto.exchanges.binance.rest_apis.spot.spot_account import spot_client_read


def get_addresses(client):
    """Gets address

    Args:
        client (_type_): binance spot client
    """
    add = client.get_deposit_address({"coin": "ETH"})
    return add


if __name__ == "__main__":

    address = get_addresses(spot_client_read)
    print(address)
