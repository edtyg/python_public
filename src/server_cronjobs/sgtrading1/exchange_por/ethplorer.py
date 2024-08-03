"""
eth explorer
free api key that has more functionality than etherscan
https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
"""

from typing import Optional

import pandas as pd
import requests
from local_credentials.api_key_data import ETHPLORER_KEY


class EthPlorer:
    """erc chain explorer"""

    def __init__(self, apikey: str):
        self.base_url = "https://api.ethplorer.io/"
        self.apikey = apikey
        self.timeout = 5

        # take note of caps in the addresses
        self.erc_tokens_contract_address = [
            "0xdac17f958d2ee523a2206206994597c13d831ec7",  # usdt
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # usdc
            "0x4fabb145d64652a948d72533023f6e7a623c7c53",  # busd
            "0x0000000000085d4780b73119b644ae5ecd22b376",  # tusd
            "0x8e870d67f660d95d5be530380d0ec0bd388289e1",  # usdp
        ]

    def get_address_info(
        self, wallet_address: str, token_address: Optional[str] = None
    ):
        """gets balances for an erc address
        can specify token contract address or leave it blank to return all

        Args:
            wallet_address (str) - erc wallet address
            token_address Optional(str) - erc_tokens_contract_address
        """
        endpoint = f"getAddressInfo/{wallet_address}"
        params = {
            "token": token_address,
            "apiKey": self.apikey,
        }
        response = requests.get(
            self.base_url + endpoint, params=params, timeout=self.timeout
        )
        return response.json()

    def get_erc20_balances(self, wallet_address: str):
        """
        pulls all token balances from above endpoint, then do a loop to filter out
        selected tokens. This reduces api call limits
        """
        df_balance = pd.DataFrame()
        data = self.get_address_info(wallet_address)

        # saving ETH balance and price
        eth_balances = data["ETH"]["balance"]
        eth_price = data["ETH"]["price"]["rate"]
        df_eth = pd.DataFrame(
            {
                "balance": eth_balances,
                "coin": "ETH",
                "wallet_address": wallet_address,
                "token_address": "",
                "decimals": 0,
                "price": eth_price
            },
            index=[0],
        )
        df_balance = pd.concat([df_balance, df_eth])
        
        try:
            other_erc_balances = data["tokens"]
            for i in other_erc_balances:
                if i["tokenInfo"]["address"] in self.erc_tokens_contract_address:
                    balance = i["balance"]
                    symbol = i["tokenInfo"]["symbol"]
                    token_address = i["tokenInfo"]["address"]
                    decimals = i["tokenInfo"]["decimals"]
                    price = i["tokenInfo"]["price"]["rate"]
    
                    df_other_erc = pd.DataFrame(
                        {
                            "balance": balance,
                            "coin": symbol,
                            "wallet_address": wallet_address,
                            "token_address": token_address,
                            "decimals": decimals,
                            "price": price,
                        },
                        index=[0],
                    )
                    df_balance = pd.concat([df_balance, df_other_erc])
        except KeyError as e:
            df_other_erc = pd.DataFrame()
            df_balance = pd.concat([df_balance, df_other_erc])
            
            
        df_balance = df_balance.fillna(0)
        try:
            df_balance["balance"] = df_balance["balance"].astype("float")
            df_balance["decimals"] = df_balance["decimals"].astype("float")
            df_balance["price"] = df_balance["price"].astype("float")
            df_balance["balance"] = df_balance["balance"] / (
                1 * 10 ** df_balance["decimals"]
            )
            df_balance["market_cap"] = df_balance["price"]  * df_balance["balance"]
            return df_balance

        except Exception as error:
            return df_balance


if __name__ == "__main__":
    client = EthPlorer(ETHPLORER_KEY)

    erc_wallet_address = "0x3c783c21a0383057d128bae431894a5c19f9cf06"
    balance_eth = client.get_erc20_balances(erc_wallet_address)
