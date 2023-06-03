"""
https://docs.osl.com/reference/introduction
api docs
"""

from osl_client import OslClient
from local_credentials.api_key_brokers import OSL_KEY, OSL_SECRET


class OslClientRest(OslClient):
    """OSL REST API client"""

    ######################
    ### brokerage REST ###
    ######################

    def get_quote(self, body: dict):
        # https://docs.osl.com/reference/get-quote
        """Get Quote - quote lasts for about 5 seconds

        Args:
            body (dict):s
            body = {
                "quoteRequest": {
                    "tradedCurrency": "USDT", # base ccy
                    "settlementCurrency": "USD", # quote ccy
                    "buyTradedCurrency": 'true', # true = buy base ccy, false = sell base ccy
                    "tradedCurrencyAmount": 1000, # float trade size in base ccy -
                            either this or settlementCurrencyAmount not both
                    "settlementCurrencyAmount": 1000 # float trade size in quote ccy -
                            either this or tradedCurrencyAmount not both
                    }
                }
        """

        method = "POST"
        path = "api/3/retail/quote"
        data = self.v3_mk_request(method, path, body)
        return data

    def execute_trade(self, body: dict):
        # https://docs.osl.com/reference/get-quote
        """Executes trade - requires quoteid

        Args:
            body (dict):
            body = {
                "tradeRequest": {"quoteId": "xxx"}
        """

        method = "POST"
        path = "api/3/retail/trade"
        data = self.v3_mk_request(method, path, body)
        return data

    def trade_limit(self, body: dict = None):
        # https://docs.osl.com/reference/get-trading-limit
        """post method"""
        method = "POST"
        path = "api/3/user/limit"
        data = self.v3_mk_request(method, path, body)
        return data

    ####################
    ### brokerage WS ###
    ####################

    def auth_token(self, body: dict = None):
        # https://docs.osl.com/reference/request-authentication-token
        """post method"""
        method = "POST"
        path = "api/3/bcg/rest/auth/token"
        data = self.v3_mk_request(method, path, body)
        return data

    ###############
    ### custody ###
    ###############

    def account_infomation(self, body: dict = None):
        # https://docs.osl.com/reference/get-account-information
        """post method"""
        method = "POST"
        path = "api/3/account"
        data = self.v3_mk_request(method, path, body)
        return data

    def transaction_list(self, body: dict = None):
        # https://docs.osl.com/reference/get-transactions
        """post method"""
        method = "POST"
        path = "api/3/transaction/list"
        data = self.v3_mk_request(method, path, body)
        return data

    def transfer_list(self, body: dict = None):
        # https://docs.osl.com/reference/get-transfers
        """post method"""
        method = "POST"
        path = "api/3/transfer/list"
        data = self.v3_mk_request(method, path, body)
        return data

    ##############
    ### public ###
    ##############

    def currency_pairs(self, body: dict = None):
        """get method"""
        method = "GET"
        path = "api/3/currencyStatic"
        data = self.v3_mk_request(method, path, body)
        return data


if __name__ == "__main__":
    client = OslClientRest(OSL_KEY, OSL_SECRET)

    account = client.account_infomation()
    print(account)

    transactions = client.transaction_list()
    print(transactions)

    # transfers = client.transfer_list()
    # ccy_pairs = client.currency_pairs()

    # get_quote1 = client.get_quote(
    #     {
    #         "quoteRequest": {
    #             "tradedCurrency": "BTC",
    #             "settlementCurrency": "USDT",
    #             "buyTradedCurrency": "false",
    #             "tradedCurrencyAmount": 1,
    #         }
    #     }
    # )

    # execute_quote1 = client.execute_trade(
    #     {"tradeRequest": {"quoteId": "xxx"}}  # FILL IN QUOTEID HERE
    # )

    trade_limits = client.trade_limit()
    print(trade_limits)
