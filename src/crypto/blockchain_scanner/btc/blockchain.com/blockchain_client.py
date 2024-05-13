"""
https://www.blockchain.com/explorer/api
API docs here - no apikey needed

docs for blockchain explorer
https://www.blockchain.com/explorer/api/blockchain_api
"""

import requests


class BlockChain:
    """
    Client to interact with BTC blockchain data
    """

    DEFAULT_TIMEOUT = 5

    def __init__(self):
        self.blockchain_base_url = "https://blockchain.info/"
        self.timeout = self.DEFAULT_TIMEOUT

    ########################
    ### Standard Request ###
    ########################

    def _get(self, endpoint: str):
        """
        Standard Get Request
        """

        try:
            response = requests.get(
                self.blockchain_base_url + endpoint, timeout=self.timeout
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()

        except requests.exceptions.Timeout:
            print("Request timed out. Please try again later.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    ###############
    ### Methods ###
    ###############

    def get_transaction(self, txid: str):
        """Gets information on BTC transaction

        Args:
            txid (str): transaction id
        """
        endpoint = f"rawtx/{txid}"
        resp = self._get(endpoint)  # Use _get method to avoid duplicate code
        return resp

    def get_block_count(self):
        """Gets current BTC block height"""
        endpoint = "q/getblockcount"
        resp = self._get(endpoint)
        return resp

    def get_num_confirmations(self, txid: str):
        """Gets number of confirmations for a txid

        Args:
            txid (str): transaction id
        """

        transaction_block = self.get_transaction(txid)
        transaction_block_height = transaction_block["block_height"]
        if transaction_block_height:
            print(f"Transaction block height = {transaction_block_height}")
            latest_block_height = self.get_block_count()
            print(f"Latest block height = {latest_block_height}")
            num_confo = latest_block_height - transaction_block_height + 1
            print(f"Number of confirmations = {num_confo}")
        else:
            num_confo = 0
            print("Transaction is unconfirmed")

        return num_confo


if __name__ == "__main__":
    client = BlockChain()

    TRANSACTION_ID1 = "c695d6c204e0571164256dd3e83acacfe95347026441877124bf5b6a0875f647"

    tx_info = client.get_transaction(TRANSACTION_ID1)
    print(tx_info)

    block_ct = client.get_block_count()
    print(block_ct)

    confirmation_count = client.get_num_confirmations(TRANSACTION_ID1)
    print(confirmation_count)
