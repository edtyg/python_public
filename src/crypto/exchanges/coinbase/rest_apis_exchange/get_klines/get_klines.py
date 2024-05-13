"""
Gets Coinbase Exchange account transfers
"""

import pandas as pd

from keys.api_work.crypto_exchanges.coinbase import COINBASE_EXCHANGE_HTS_READ
from src.crypto.exchanges.coinbase.rest.coinbase_exchange_client import CoinbaseExchange


def get_klines(client):
    data = client.get_product_candles("BTCUSDT")
    return data


if __name__ == "__main__":
    account = COINBASE_EXCHANGE_HTS_READ
    client = CoinbaseExchange(
        account["api_key"],
        account["api_secret"],
        account["passphrase"],
    )

    data = get_klines(client)
    print(data)
