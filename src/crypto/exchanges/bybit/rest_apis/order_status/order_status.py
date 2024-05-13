"""
Bybit Spot Account balances
"""

from local_credentials.api_work.crypto_exchanges.bybit import BYBIT_MCA_MAIN_TRADE
from python.crypto.exchanges.bybit.rest.bybit_client import Bybit


def check_open_orders(client):
    """
    Check on current open orders

    Args:
        client (_type_): bybit spot client
    """
    open_orders = client.get_open_orders(
        {
            "category": "spot",
            "symbol": "ETHUSDT",
        }
    )
    return open_orders


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_TRADE
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    check_open_orders = check_open_orders(client)
    print(check_open_orders)
