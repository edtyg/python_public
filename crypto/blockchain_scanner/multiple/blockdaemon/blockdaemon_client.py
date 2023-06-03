"""
https://docs.blockdaemon.com/reference/ubiquity-quick-start
"""
import requests
from local_credentials.api_key_data import BLOCKDAEMON_KEY


class BlockDaemon:
    """rest api for onchain data"""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://svc.blockdaemon.com/universal"
        self.header = {"Authorization": f"Bearer {self.api_key}"}
        self.timeout = 5

    def get_protocols(self):
        """
        GET Protocols Overview
        https://docs.blockdaemon.com/reference/universal-compute-units
        """
        endpoint = "/v1/"

        response = requests.request(
            "GET", self.base_url + endpoint, headers=self.header, timeout=self.timeout
        )
        data = response.json()
        return data

    def get_balances(self, protocol: str, network: str, address: str):
        """
        Get a List of Balances for an Address
        https://docs.blockdaemon.com/reference/universal-compute-units
        """
        endpoint = f"/v1/{protocol}/{network}/account/{address}"

        response = requests.request(
            "GET", self.base_url + endpoint, headers=self.header, timeout=self.timeout
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = BlockDaemon(BLOCKDAEMON_KEY)

    protocols = client.get_protocols()
