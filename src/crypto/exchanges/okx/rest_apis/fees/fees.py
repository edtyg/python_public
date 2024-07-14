"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.okx import OKX_MCA_LTP1_READ
from src.crypto.exchanges.okx.rest.okx_client import Okx


def fee(client):
    """Gets maximul loan amt

    Args:
        client (_type_): okx spot client
    """
    data = client.get_fees({"instType": "SPOT", "instId": "BTC-USDT"})
    return data


if __name__ == "__main__":
    account = OKX_MCA_LTP1_READ
    okx_client = Okx(
        apikey=account["api_key"],
        apisecret=account["api_secret"],
        passphrase=account["passphrase"],
    )

    trading_fees = fee(okx_client)
    print(trading_fees)
