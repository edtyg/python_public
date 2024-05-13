"""
Get account ids and account details
"""

from local_credentials.api_personal.forex_brokers.oanda import OANDA_DEMO, OANDA_TRADE
from python.forex.oanda.rest.oanda_client import Oanda

if __name__ == "__main__":
    account = OANDA_DEMO
    client = Oanda(account["api_key"])

    # get all accounts
    accounts = client.get_accounts()
    print(accounts)

    # get account by id
    # account_id = client.get_account_by_id("101-003-13096092-001")
    # print(account_id)

    # get summary of account by id
    # account_summary = client.get_account_summary("101-003-13096092-001")
    # print(account_summary)
