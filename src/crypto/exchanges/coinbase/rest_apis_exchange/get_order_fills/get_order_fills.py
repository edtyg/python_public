"""
Gets fills
"""

import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_exchanges.coinbase import (
    COINBASE_EXCHANGE_HTS_READ,
)
from python.crypto.exchanges.coinbase.rest.coinbase_exchange_client import (
    CoinbaseExchange,
)


def get_fills(client):
    """Gets ledger records for a single currency

    Args:
        client (_type_): coinbase exchange client
    """
    df_final = pd.DataFrame()
    after_trade_id = None
    fills_params = {"product_id": "USDT-USD"}

    status = False
    while status is False:
        if after_trade_id is None:
            fills = client.get_all_fills(fills_params)
            if fills:
                df_fills = pd.DataFrame(fills)
                after_trade_id = df_fills.tail(1)["trade_id"].values[0]
                df_final = pd.concat([df_final, df_fills])
                fills_params["after"] = after_trade_id
            else:
                status = True
                continue

        else:
            fills = client.get_all_fills(fills_params)
            if fills:
                df_fills = pd.DataFrame(fills)
                after_trade_id = df_fills.tail(1)["trade_id"].values[0]
                df_final = pd.concat([df_final, df_fills])
                fills_params["after"] = after_trade_id
            else:
                status = True
                continue
        print(df_fills)
    return df_final


if __name__ == "__main__":
    account = COINBASE_EXCHANGE_HTS_READ
    client = CoinbaseExchange(
        account["api_key"],
        account["api_secret"],
        account["passphrase"],
    )

    df = get_fills(client)
    print(df)
