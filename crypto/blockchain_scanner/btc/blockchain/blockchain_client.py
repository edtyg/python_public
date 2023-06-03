"""
https://www.blockchain.com/explorer/api
API docs here - no apikey needed
"""
import requests


class BlockChain:
    """
    client to interact with btc blockchain data
    """

    def __init__(self):
        self.base_url = "https://blockchain.info/"
        self.timeout = 5

    def get_transaction(self, txid: str):
        """Gets infomation on btc transaction

        Args:
            txid (str): transaction id
        """
        endpoint = f"rawtx/{txid}"
        resp = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return resp.json()

    def get_block_count(self):
        """Gets current btc block height"""
        endpoint = "q/getblockcount"
        resp = requests.get(self.base_url + endpoint, timeout=self.timeout)
        return resp.json()

    def get_num_confirmations(self, txid: str):
        """Gets number of confirmations for a txid

        Args:
            txid (str): transaction id
        """

        transaction_block = self.get_transaction(txid)
        transaction_block_height = transaction_block["block_height"]
        if transaction_block_height:
            print(f"transaction block height = {transaction_block_height}")
            latest_block_height = self.get_block_count()
            print(f"latest block height = {latest_block_height}")
            num_confo = latest_block_height - transaction_block_height + 1
            print(f"number of confirmations = {num_confo}")
        else:
            num_confo = 0
            print("transaction is unconfirmed")

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
