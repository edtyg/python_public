"""
blockchain explorer api
https://www.blockchain.com/explorer/api/blockchain_api
only for pulling wallet BTC balances
"""

import requests
import pandas as pd


class BlockChain:
    """api from blockchain.com"""

    def __init__(self):
        self.base_url = "https://blockchain.info"
        self.base_url_exchange = "https://api.blockchain.com/v3/exchange"
        self.timeout = 5

    def get_btc_price(self):
        """gets btc-usd price from blockchain.com"""

        endpoint = "/tickers/BTC-USD"
        response = requests.get(self.base_url_exchange + endpoint, timeout=self.timeout)
        data = response.json()["last_trade_price"]
        return data

    def get_balance(self, address: str):
        """
        balances are in satoshis - 100,000,000
        100 mil satoshi = 1 BTC
        """
        response = requests.get(
            self.base_url + "/balance", params={"active": address}, timeout=self.timeout
        )
        data = response.json()[address]
        balance = data["final_balance"] / 100000000

        df_data = pd.DataFrame(
            {
                "balance": balance,
                "coin": "BTC",
                "wallet_address": address,
                "token_address": "",
                "decimals": 0,
                "price": self.get_btc_price(),
            },
            index=[0],
        )
        df_data["market_cap"] = df_data["balance"] * df_data["price"]
        
        return df_data


if __name__ == "__main__":
    ADDRESS = "12qTdZHx6f77aQ74CPCZGSY47VaRwYjVD8"

    client = BlockChain()
    btc_price = client.get_btc_price()
    print(btc_price)

    balance_btc = client.get_balance(ADDRESS)
    print(balance_btc)
