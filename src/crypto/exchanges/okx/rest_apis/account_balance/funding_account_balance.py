"""
SPOT execution program
"""
import datetime as dt

import pandas as pd

from local_credentials.api_work.crypto_exchanges.okx import OKX_MCA_MAIN_READ
from python.crypto.exchanges.okx.rest.okx_client import Okx


def get_funding_account_balances(client):
    """Gets funding account balances

    Args:
        client (_type_): okx spot client
    """
    curr_time = dt.datetime.now()
    funding_balances = client.get_balance_funding()
    data = funding_balances["data"]
    df_funding_balances = pd.DataFrame(data)

    df_funding_balances["datetime"] = curr_time
    return df_funding_balances


if __name__ == "__main__":
    okx_client = Okx(
        apikey=OKX_MCA_MAIN_READ["api_key"],
        apisecret=OKX_MCA_MAIN_READ["api_secret"],
        passphrase=OKX_MCA_MAIN_READ["passphrase"],
    )

    funding_balance = get_funding_account_balances(okx_client)
    print(funding_balance)
