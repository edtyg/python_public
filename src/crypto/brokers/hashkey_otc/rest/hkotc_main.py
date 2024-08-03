"""
binance api docs here
https://www.binance.com/en/binance-api
"""

from typing import Dict, Optional

from crypto.brokers.hashkey_otc.rest.hkotc_client import HashkeyOTC
from keys.api_work.crypto_brokers.hashkey_otc import HASHKEY_OTC_TRADE


class HashkeyOTCSpot(HashkeyOTC):
    """
    Client to interact with hashkey otc APIs
    """

    def __init__(self, apikey: str = None, apisecret: str = None):
        super().__init__(apikey, apisecret)
        self.hashkey_otc_base_url = "https://api.hts.sg"

    ###################
    ### Public Data ###
    ###################

    def get_symbols(self, params: Optional[Dict] = None) -> dict:
        """Retrieve a list of symbols with open contracts
        https://qa-docs.hts.sg/#tag/Public-Data/operation/getSymbols

        Args:
            params (Optional[Dict], optional): Defaults to None.
            name        type    required    desc            example
            symbol      str     no          trade symbol    BTC-USD, BTC-USDT
        """
        endpoint = "/v1/unify/symbols"
        return self.rest_requests("GET", self.hashkey_otc_base_url, endpoint, params)

    def get_indicative_price(self, params: dict) -> dict:
        """
        Retrieve index tickers.
        https://qa-docs.hts.sg/#tag/Public-Data/operation/getIndicativePrice

        Args:
            params (dict):
            name        type    required    desc            example
            symbol      str     yes         trade symbol    BTC-USD, BTC-USDT
        """
        endpoint = "/v1/unify/indicative_prices"
        return self.rest_requests("GET", self.hashkey_otc_base_url, endpoint, params)

    ###############
    ### Account ###
    ###############

    def get_balance(self, params: Optional[Dict] = None) -> dict:
        """
        Retrieve the funding account balances of all
        the assets and the amount that is available or on hold.
        https://qa-docs.hts.sg/#tag/Account/operation/getBalance

        Args:
            params (dict):
            name        type    required    desc            example
            ccy         str     no         trade symbol    BTC-USD, BTC-USDT
        """
        endpoint = "/v1/unify/balances"
        return self.rest_requests("GET", self.hashkey_otc_base_url, endpoint, params)

    def get_transfers(self, params: Optional[Dict] = None) -> dict:
        """
        Transfers reporting and tracking.
        https://qa-docs.hts.sg/#tag/Account/operation/getAccountTransfer

        Args:
            params (dict):
            name        type    required    desc                example
            ccy         str     no          trade symbol        BTC-USD, BTC-USDT
            type        str     no          type of transf      deposit, withdrawal, refund
            start_time  str     no          unix time in ms     1654041600000
            end_time    str     no          unix time in ms     1654041600000
            from        str     no          from id
            limit       str     no          num of req          default 100, max 100
        """
        endpoint = "/v1/unify/transfer/history"
        return self.rest_requests("GET", self.hashkey_otc_base_url, endpoint, params)

    #############
    ### Trade ###
    #############

    def post_create_rfq(self, params: Optional[Dict] = None) -> dict:
        """
        Creates a new RFQ
        https://qa-docs.hts.sg/#tag/Trade/operation/createRFQ

        Args:
            params (dict):
            name        type    required    desc                    example
            rfq_id      str     yes         client supplied id      test_order1
            symbol      str     yes         symbol                  BTC-USD
            side        str     yes                                 buy or sell
            target_size str     yes         size                    10
            target_ccy  str     yes         base or quote           base_ccy or quote_ccy
        """
        endpoint = "/v1/unify/quote"
        return self.rest_requests("POST", self.hashkey_otc_base_url, endpoint, params)


if __name__ == "__main__":
    key = HASHKEY_OTC_TRADE
    client = HashkeyOTCSpot(key["api_key"], key["api_secret"])

    # data = client.get_symbols({"symbol": "BTC-USD"})
    # print(data)

    # indic_px = client.get_indicative_price({"symbol": "BTC-USD"})
    # print(indic_px)

    # bal = client.get_balance()
    # print(bal)

    # transf = client.get_transfers()
    # print(transf)

    rfq1 = client.post_create_rfq(
        {
            # "rfq_id": "test",
            # "symbol": "BTC-USD",
            # "side": "buy",
            # "target_size": "1",
            # "target_ccy": "base_ccy",
        }
    )
    print(rfq1)
