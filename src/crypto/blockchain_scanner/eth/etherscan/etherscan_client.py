"""
https://docs.etherscan.io/
api docs for etherscan
using free API key
certain endpoints require a PRO subscription - paid API key
"""

import requests

from keys.api_personal.crypto_blockchain.etherscan import ETHERSCAN_KEY


class EtherScan:
    """etherscan rest api"""

    def __init__(self, apikey: str):
        self.base_url = "https://api.etherscan.io/api"
        self.apikey = apikey
        self.timeout = 5

    ################
    ### accounts ###
    ################

    def get_ether_balance(self, address: str):
        """Get Ether Balance for a Single Address
        https://docs.etherscan.io/api-endpoints/accounts
        """
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": self.apikey,
        }
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        return response.json()

    def get_transactions(self, address: str):
        """Get a list of 'Normal' Transactions By Address
        https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address
        """
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "tag": "latest",
            "sort": "desc",
            "apikey": self.apikey,
        }
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        return response.json()

    def get_internal_transactions(self, address: str):
        """Get a list of 'Internal' Transactions by Address
        https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-internal-transactions-by-address
        """
        params = {
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "tag": "latest",
            "sort": "desc",
            "apikey": self.apikey,
        }
        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        return response.json()


if __name__ == "__main__":
    client = EtherScan(ETHERSCAN_KEY)

    eth_address = ""

    eth_balance = client.get_ether_balance(eth_address)
    normal_transaction = client.get_transactions(eth_address)
    internal_transaction = client.get_internal_transactions(eth_address)
