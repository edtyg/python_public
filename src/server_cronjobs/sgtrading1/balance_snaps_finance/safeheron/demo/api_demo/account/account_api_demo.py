import os
import sys

import yaml

from src.server_cronjobs.sgtrading1.balance_snaps_finance.safeheron.safeheron_api_sdk_python.api.account_api import *

full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"
file_path = save_path
print(file_path)


def read_yaml(file_path):
    with open(file_path + "config.yaml", "r") as f:
        return yaml.safe_load(f)


class TestAccount:
    def test_list_accounts(self):
        config = read_yaml(file_path)
        account_api = AccountApi(config)
        param = ListAccountRequest()
        param.pageSize = 10
        param.pageNumber = 1
        res = account_api.list_accounts(param)
        return res

    # def test_create_account(self):
    #     config = read_yaml(file_path)
    #     account_api = AccountApi(config)
    #     param = CreateAccountRequest()
    #     param.accountName = "accountNameTest"
    #     res = account_api.create_account(param)
    #     print(res)

    def test_list_account_coins(self, account_key: str):
        config = read_yaml(file_path)
        account_api = AccountApi(config)
        param = ListAccountCoinRequest()
        param.accountKey = account_key
        res = account_api.list_account_coin(param)
        return res


if __name__ == "__main__":
    client = TestAccount()

    # accounts = client.test_list_accounts()
    # print(accounts)

    # account3642c2bc2b5b4d4183c7127f58b1ce8a
    # account36670f9775ff4dad88b5246f01d713e5

    account_coins = client.test_list_account_coins(
        "account36670f9775ff4dad88b5246f01d713e5"
    )
    print(account_coins)
