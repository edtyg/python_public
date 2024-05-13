"""
https://solana.com/docs/rpc/http
"""

import requests


class SolanaClient:
    """
    client to interact with btc blockchain data
    """

    def __init__(self):
        self.base_url = "https://api.devnet.solana.com"
        self.timeout = 3
        self.headers = {
            "Content-Type": "application/json",
        }
        self.data = {
            # "jsonrpc": "2.0",
            "id": 1,
        }

    def get_account_info(self):
        """
        Returns all information associated with the account of provided Pubkey
        https://solana.com/docs/rpc/http/getaccountinfo

        """
        method = "getAccountInfo"
        self.data["method"] = method

        address = "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"
        self.data["params"] = address
        print(self.data)

        response = requests.post(
            self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            data=self.data,
        )
        return response.json()


if __name__ == "__main__":
    client = SolanaClient()

    bal = client.get_account_info()
    print(bal)
