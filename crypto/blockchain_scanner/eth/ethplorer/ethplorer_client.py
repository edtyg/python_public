"""
eth explorer
free api key that has more functionality than etherscan
https://github.com/EverexIO/Ethplorer/wiki/Ethplorer-API
"""
import requests

from local_credentials.api_key_data import ETHPLORER_KEY


class ETHPlorer:
    """erc chain explorer"""

    def __init__(self):
        self.base_url = "https://api.ethplorer.io/"
        self.apikey = ETHPLORER_KEY
        self.timeout = 5

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


if __name__ == "__main__":
    client = ETHPlorer()

    ADDRESS = ""
    TOKEN_ADDRESS = "0x70e8de73ce538da2beed35d14187f6959a8eca96"  # xsgd
    LIMIT = 1000

    address_info = client.get_address_info(ADDRESS)
    token_hist = client.get_token_history(TOKEN_ADDRESS, LIMIT)
    address_hist = client.get_address_history(ADDRESS, LIMIT)
    address_tx = client.get_address_transactions(ADDRESS, LIMIT)
