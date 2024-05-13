"""
Coinbase Brokerage Tradeable Pairs
"""

import pandas as pd

from local_credentials.api_personal.crypto_exchanges.coinbase import (
    COINBASE_BROKERAGE_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_brokerage_client import (
    CoinbaseBrokerage,
)


def get_coinbase_products(client):
    """
    Gets Coinbase Brokerage trading pairs

    Args:
        client (_type_): coinbase brokerage spot client
    """

    all_products = client.list_products()
    df_all_products = pd.DataFrame(all_products["products"])

    return df_all_products


if __name__ == "__main__":
    account = COINBASE_BROKERAGE_READ
    coinbase_client = CoinbaseBrokerage(
        account["api_key"],
        account["api_secret"],
    )

    df = get_coinbase_products(coinbase_client)
    print(df)
