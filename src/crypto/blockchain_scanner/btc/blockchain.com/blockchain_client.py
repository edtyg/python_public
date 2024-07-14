"""
blockchain.com APIs
https://www.blockchain.com/explorer/api/blockchain_api
"""

import requests

from src.utils.utils import Utils


class BlockChain:
    """
    Client to interact with BTC blockchain data
    """

    DEFAULT_TIMEOUT = 5

    def __init__(self):
        self.blockchain_base_url = "https://blockchain.info/"

    ###############
    ### Methods ###
    ###############

    def get_transaction(self, txid: str):
        """Gets information on BTC transaction

        Args:
            txid (str): transaction id
        """
        endpoint = f"rawtx/{txid}"
        return Utils.get_request(self.blockchain_base_url, endpoint)

    def get_block_count(self):
        """Gets current BTC block height"""
        endpoint = "q/getblockcount"
        return Utils.get_request(self.blockchain_base_url, endpoint)

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
