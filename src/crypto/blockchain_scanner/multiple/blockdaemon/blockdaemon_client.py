"""
https://docs.blockdaemon.com/reference/blockdaemon-api-suite
https://solana.com/docs/rpc#methods - for solana methods

each solana wallet may have SOL balances as well as SPL (Solana Program Library) tokens
SPL tokens refer to fungible tokens on Solana (like erc-20 tokens)

"""

import requests

from local_credentials.api_personal.crypto_blockchain.blockdaemon import BLOCKDAEMON_KEY


class BlockDaemon:
    """rest api for onchain data"""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.solana_base_url = "https://svc.blockdaemon.com/solana/mainnet/native"
        self.header = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = 3

    ############################
    ### Standard Post Method ###
    ############################

    def _post(self, params: str):
        """Standard post method"""
        response = requests.post(
            self.solana_base_url,
            headers=self.header,
            json=params,
            timeout=self.timeout,
        )
        return response.json()

    ###############
    ### methods ###
    ###############

    def get_account_info(self):
        """
        Returns all information associated with the account of provided Pubkey
        input = Public Address of any wallet

        https://solana.com/docs/rpc/http/getaccountinfo
        """
        params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": ["BMHwZHgEe32LSbF8VrkpVVsD4NN1s8zD9kersLBkGcDd"],
        }
        return self._post(params)

    def get_balance(self):
        """
        Returns the lamport balance of the account of provided Pubkey
        i.e 1 Solana = 1B lamport
        input = Public Address of any wallet

        https://solana.com/docs/rpc/http/getbalance
        """
        params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": ["BMHwZHgEe32LSbF8VrkpVVsD4NN1s8zD9kersLBkGcDd"],
        }
        return self._post(params)

    def get_token_account_balance(self):
        """
        Returns the token balance of an SPL Token account.
        https://solana.com/docs/rpc/http/getbalance
        input = SPL token account of an address
        Each Solana wallet has a unique SPL token account for each token

        """
        params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountBalance",
            "params": ["FDFqXGDwXxEuuvnEeB3cUF2fKPF8HKddG8MFNJnCLxSJ"],
        }
        return self._post(params)

    def get_token_account_by_owner(self):
        """
        Returns all SPL Token accounts by token owner.
        https://solana.com/docs/rpc/http/gettokenaccountsbyowner
        input = Public Address of any wallet
        """
        params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                "BMHwZHgEe32LSbF8VrkpVVsD4NN1s8zD9kersLBkGcDd",
                {
                    "mint": "7atgF8KQo4wJrD5ATGX7t1V2zVvykPJbFfNeVf1icFv1",
                },
                {"encoding": "jsonParsed"},
            ],
        }
        return self._post(params)


if __name__ == "__main__":
    client = BlockDaemon(BLOCKDAEMON_KEY["api_key"])

    # account_info = client.get_account_info()
    # print(account_info)

    # balance = client.get_balance()
    # print(balance)

    # token_acc_balance = client.get_token_account_balance()
    # print(token_acc_balance)

    spl_accounts = client.get_token_account_by_owner()
    print(spl_accounts)
