"""
https://www.oklink.com/docs/en/#introduction
"""

import requests

from local_credentials.api_personal.crypto_blockchain.oklink import OKLINK_KEY


class OkLink:
    """rest api for onchain data"""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://www.oklink.com"
        self.header = {"Ok-Access-Key": self.api_key}
        self.timeout = 5

    def _get(self, endpoint: str):
        """standard get method"""
        response = requests.get(
            self.base_url + endpoint,
            headers=self.header,
            timeout=self.timeout,
        )
        return response.json()

    ### Market Data ###
    def get_supported_chains(self):
        """
        Get the list of public chains supported in this module,
        which can be used to query the chainID of a specific chain.
        Return in alphabetical order based on the first letter of chainShortName by default.

        https://www.oklink.com/docs/en/#market-data-supported-chains

        {'chainId': '0', 'chainFullName': 'Bitcoin', 'chainShortName': 'BTC'}
        {'chainId': '1', 'chainFullName': 'Ethereum', 'chainShortName': 'ETH'}
        {'chainId': '501', 'chainFullName': 'Solana', 'chainShortName': 'SOL'}
        """
        endpoint = "/api/v5/explorer/tokenprice/chain-list"
        return self._get(endpoint)


if __name__ == "__main__":
    client = OkLink(OKLINK_KEY["api_key"])

    chains = client.get_supported_chains()
    print(chains)
