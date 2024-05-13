"""
Cancel orders
"""

from local_credentials.api_personal.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_TRADE,
)
from python.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def cancel_order(client):
    """
    Cancels order on brokerage account

    Args:
        client (_type_): coinbase brokerage client

    """

    cancel_brokerage_order = client.cancel_orders(
        params={"order_ids": ["74c558e9-4099-4a03-b699-d71330f34198"]}
    )
    print(cancel_brokerage_order)
    return cancel_brokerage_order


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_TRADE
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    cancel_order1 = cancel_order(coinbase_client)
