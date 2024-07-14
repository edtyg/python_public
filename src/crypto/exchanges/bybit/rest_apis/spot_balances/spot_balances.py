"""
Bybit Spot Account balances
"""

import pandas as pd

from crypto.exchanges.bybit.rest.bybit_client import Bybit
from keys.api_work.crypto_exchanges.bybit import BYBIT_MCA_LTP1_READ


def check_account_balances(client):
    """
    Check on current bal

    Args:
        client (_type_): bybit spot client
    """
    funding_balance = client.get_all_coins_balance({"accountType": "FUND"})["result"][
        "balance"
    ]
    uta_balance = client.get_all_coins_balance({"accountType": "UNIFIED"})["result"][
        "balance"
    ]
    print(uta_balance)
    response = {"funding": funding_balance, "uta": uta_balance}
    df_final = pd.DataFrame()
    for key, value in response.items():
        df_bal = pd.DataFrame(value)
        df_bal["walletBalance"] = df_bal["walletBalance"].astype("float")
        df_bal = df_bal.loc[df_bal["walletBalance"] != 0]
        df_bal["account_type"] = key
        df_bal.reset_index(drop=True, inplace=True)
        df_final = pd.concat([df_final, df_bal])
    return df_final


if __name__ == "__main__":
    account = BYBIT_MCA_LTP1_READ
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    balances = check_account_balances(client)
    print(balances)
