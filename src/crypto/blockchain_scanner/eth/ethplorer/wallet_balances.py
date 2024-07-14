"""
Gets wallet balances using ethplorer api
"""

import pandas as pd

from keys.api_personal.crypto_blockchain.ethplorer import ETHPLORER_KEY
from src.crypto.blockchain_scanner.eth.ethplorer.ethplorer_client import ETHPlorer
from src.crypto.blockchain_scanner.eth.ethplorer.ethplorer_contract_credentials import (
    erc_tokens_addresses,
    erc_wallet_addresses,
)


def get_wallet_balances(client):
    """
    Returns wallet balances and addresses
    """
    df_final = pd.DataFrame()
    for wallet_name, wallet_address in erc_wallet_addresses.items():
        print(wallet_name, wallet_address)
        address_info = client.get_address_info(wallet_address)
        eth_balance = address_info["ETH"]["balance"]
        data_eth = {
            "balance": float(eth_balance),
            "token_address": "NA",
            "token_decimals": 0,
            "token_symbol": "ETH",
            "wallet_name": wallet_name,
            "wallet_address": wallet_address,
        }
        df_data_eth = pd.DataFrame(data_eth, index=[0])
        df_final = pd.concat([df_final, df_data_eth])

        try:
            tokens_list = address_info["tokens"]
        except:
            print("no other erc tokens for this address")
            tokens_list = []

        if tokens_list:
            for tokens in tokens_list:
                token_balance = float(tokens["balance"])
                token_address = tokens["tokenInfo"]["address"]
                token_decimals = int(tokens["tokenInfo"]["decimals"])
                token_symbol = tokens["tokenInfo"]["symbol"]

                data_tokens = {
                    "balance": token_balance,
                    "token_address": token_address,
                    "token_decimals": token_decimals,
                    "token_symbol": token_symbol,
                    "wallet_name": wallet_name,
                    "wallet_address": wallet_address,
                }
                df_data_tokens = pd.DataFrame(data_tokens, index=[0])
                df_final = pd.concat([df_final, df_data_tokens])

    df_final.reset_index(drop=True, inplace=True)
    for i in df_final.index:
        decimal = df_final.loc[i, "token_decimals"]
        balance = df_final.loc[i, "balance"]
        multiplier = 1 * 10**decimal
        adjusted_balance = balance / multiplier
        df_final.loc[i, "adjusted_balance"] = adjusted_balance

    return df_final


if __name__ == "__main__":
    client = ETHPlorer(ETHPLORER_KEY["api_key"])

    df_wallet_balances = get_wallet_balances(client)
    print(df_wallet_balances)
