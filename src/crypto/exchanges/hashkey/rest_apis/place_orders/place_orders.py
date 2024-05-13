"""
Placing Spot Orders
"""

from local_credentials.api_personal.crypto_exchanges.hashkey import (
    HASHKEY_GLOBAL_TRADE,
    HASHKEY_GLOBAL_TRADE_MUM,
)
from python.crypto.exchanges.hashkey.rest.hashkey_global.hashkey_spot_global import (
    HashkeySpot,
)

if __name__ == "__main__":
    account = HASHKEY_GLOBAL_TRADE
    client = HashkeySpot(
        account["api_key"],
        account["api_secret"],
    )

    place_order = client.post_create_order(
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "type": "LIMIT",
            "quantity": 0.05,
            "price": 3100,
            "timeInForce": "GTC",
        }
    )
    print(place_order)
