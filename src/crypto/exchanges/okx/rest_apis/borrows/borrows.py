"""
SPOT execution program
"""

import datetime as dt

import pandas as pd

from keys.api_work.crypto_exchanges.okx import OKX_MCA_LTP1_READ
from src.crypto.exchanges.okx.rest.okx_client import Okx


def max_loan(client):
    """Gets maximul loan amt

    Args:
        client (_type_): okx spot client

    Seems like Max borrows based on master acc's limits (i.e our own)
    not LTP's

    https://www.okx.com/fees/margin
    """
    data = client.get_borrow_interest_limit(
        {
            "type": 2,
            "ccy": "USDT",
        }
    )
    return data


if __name__ == "__main__":
    account = OKX_MCA_LTP1_READ
    okx_client = Okx(
        apikey=account["api_key"],
        apisecret=account["api_secret"],
        passphrase=account["passphrase"],
    )

    loan = max_loan(okx_client)
    print(loan)
