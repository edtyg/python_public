"""
eth explorer
free api key that has more functionality than etherscan
https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
"""

import requests


class ETHPlorer:
    """erc chain explorer"""

    def __init__(self, api_key: str):
        self.base_url = "https://api.ethplorer.io/"
        self.apikey = api_key
        self.timeout = 3

    def get_address_info(self, wallet_address: str):
        """
        Returns information about an address.
        """
        endpoint = f"getAddressInfo/{wallet_address}"
        params = {
            "apiKey": self.apikey,
        }
        response = requests.get(
            self.base_url + endpoint, params=params, timeout=self.timeout
        )
        return response.json()

    def get_token_history(self, token_address: str, limit: int):
        """
        Returns a list of the last operations on a token.
        """
        endpoint = f"getTokenHistory/{token_address}"
        params = {
            "apiKey": self.apikey,
            "limit": 1000,
        }

        response = requests.get(
            self.base_url + endpoint, params=params, timeout=self.timeout
        )
        return response.json()

    def get_address_history(self, wallet_address: str, limit: int):
        """
        Returns a list of the last operations involving an address.
        """
        endpoint = f"getAddressHistory/{wallet_address}"
        params = {
            "apiKey": self.apikey,
            "limit": 1000,
        }

        response = requests.get(
            self.base_url + endpoint, params=params, timeout=self.timeout
        )
        return response.json()

    def get_address_transactions(self, wallet_address: str, limit: int):
        """
        Returns list of transactions for a specified address.
        """
        endpoint = f"getAddressTransactions/{wallet_address}"
        params = {
            "apiKey": self.apikey,
            "limit": 1000,
        }

        response = requests.get(
            self.base_url + endpoint, params=params, timeout=self.timeout
        )
        return response.json()
