"""
Gets Coinbase Exchange account transfers
"""

import pandas as pd

from keys.api_work.crypto_exchanges.coinbase import COINBASE_EXCHANGE_HTS_READ
from src.crypto.exchanges.coinbase.rest.coinbase_exchange_client import CoinbaseExchange


def get_all_account_transfers(client):
    """Gets balances

    Args:
        client (_type_): binance spot client

    "deposit", "withdraw","internal_deposit", "internal_withdraw"


    coinbase_brokerage
    BTC: 5d37db93-a9f2-5b94-8558-f45562c55c42
    ETH: f8ff3439-4977-508d-94b6-fb88fce66729
    USD: 8b6a9092-fd64-5885-b6ad-e02572b0ffa1
    USDC: 5eb08983-0f9b-5eba-a003-d1665781d49c
    USDT: f5217a41-58f6-5d1f-9d09-14070187455c

    coinbase_exchange
    BTC: 2a6e82b1-442a-4061-9673-b9e04150ba96
    ETH: 99ab0bf7-cc5c-4d4b-9613-5672c899709d
    USD: 32ba4ec5-a43a-4bbf-b526-ebdcda1d8b83
    USDC: d04b51ca-4e71-40f6-8363-6a59afba968e
    USDT: ed28240e-07a9-4acc-af62-722f671e5733
    """
    all_transfers = client.get_all_transfers({"limit": 100, "type": "withdraw"})
    coinbase_brokerage_acc = {
        "BTC": "5d37db93-a9f2-5b94-8558-f45562c55c42",
        "ETH": "f8ff3439-4977-508d-94b6-fb88fce66729",
        "USD": "8b6a9092-fd64-5885-b6ad-e02572b0ffa1",
        "USDC": "5eb08983-0f9b-5eba-a003-d1665781d49c",
        "USDT": "f5217a41-58f6-5d1f-9d09-14070187455c",
    }

    coinbase_exchange_acc = {
        "BTC": "2a6e82b1-442a-4061-9673-b9e04150ba96",
        "ETH": "99ab0bf7-cc5c-4d4b-9613-5672c899709d",
        "USD": "32ba4ec5-a43a-4bbf-b526-ebdcda1d8b83",
        "USDC": "d04b51ca-4e71-40f6-8363-6a59afba968e",
        "USDT": "ed28240e-07a9-4acc-af62-722f671e5733",
    }

    df_transf = pd.DataFrame(all_transfers)
    for i in df_transf.index:
        details = df_transf.loc[i, "details"]

    return df_transf


if __name__ == "__main__":
    account = COINBASE_EXCHANGE_HTS_READ
    client = CoinbaseExchange(
        account["api_key"],
        account["api_secret"],
        account["passphrase"],
    )

    trans = get_all_account_transfers(client)
    print(trans)
