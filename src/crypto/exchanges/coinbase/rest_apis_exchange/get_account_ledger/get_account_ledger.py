"""
Gets Coinbase Exchange account ledger for single currency
"""

import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_exchanges.coinbase import (
    COINBASE_EXCHANGE_HTS_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_exchange_client import (
    CoinbaseExchange,
)


def get_ccy_ledger(client):
    """Gets ledger records for a single currency

    Args:
        client (_type_): coinbase exchange client

    USD: 32ba4ec5-a43a-4bbf-b526-ebdcda1d8b83
    USDT: ed28240e-07a9-4acc-af62-722f671e5733
    USDC: d04b51ca-4e71-40f6-8363-6a59afba968e"
    """
    records = client.get_single_account_ledger("d04b51ca-4e71-40f6-8363-6a59afba968e")
    df_records = pd.DataFrame(records)
    df_conversions = df_records.loc[df_records["type"] == "conversion"]
    return df_conversions


if __name__ == "__main__":
    account = COINBASE_EXCHANGE_HTS_READ
    client = CoinbaseExchange(
        account["api_key"],
        account["api_secret"],
        account["passphrase"],
    )

    ledger_record = get_ccy_ledger(client)
    print(ledger_record)
