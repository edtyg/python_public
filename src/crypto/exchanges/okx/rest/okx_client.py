"""
OKX V5 API
https://www.okx.com/docs-v5/en/#overview
"""

import base64
import datetime as dt
import hmac
import json
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


class Okx:
    """Rest APIs for okx v5"""

    def __init__(self, apikey: str, apisecret: str, passphrase: str):
        self.okx_base_url = "https://www.okx.com"

        self.apikey = apikey
        self.apisecret = apisecret
        self.passphrase = passphrase
        self.headers = {
            "OK-ACCESS-KEY": self.apikey,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "CONTENT-TYPE": "application/json",
        }
        self.timeout = 3
        self.url_payload = None

    ######################
    ### Authentication ###
    ######################

    def get_current_timestamp(self) -> str:
        """
        gets current timestamp with millisecond ISO format
        e.g. 2020-12-08T09:08:57.715Z
        """
        curr_time_utc = dt.datetime.utcnow()
        curr_time_utc_iso = curr_time_utc.isoformat("T", "milliseconds")
        timestamp_iso = curr_time_utc_iso + "Z"
        return timestamp_iso

    def sign(self, message: str):
        """signing message with secret key"""
        secret_bytes = bytes(self.apisecret, encoding="utf8")
        message_bytes = bytes(message, encoding="utf8")
        signature_hash = hmac.new(
            secret_bytes,
            message_bytes,
            digestmod="sha256",
        )
        signature_digest = signature_hash.digest()
        return base64.b64encode(signature_digest)

    def hashing(self, request_type: str, endpoint: str, params: dict = None) -> str:
        """setting up headers for requests
        some slight differences for post and get requests for okx

        Args:
            request_type (str): "GET" or "POST" must be in caps
            endpoint (str): '/api/v5/account/balance?ccy=BTC' with params
            params (dict, optional): Defaults to None.

        Returns:
            str: _description_
        """
        timestamp = self.get_current_timestamp()

        if request_type.upper() == "GET" and params is None:
            message = timestamp + "GET" + endpoint

        elif request_type.upper() == "GET" and params is not None:
            message = timestamp + "GET" + endpoint + "?" + urlencode(params)

        elif request_type.upper() == "POST" and params is None:
            message = timestamp + "POST" + endpoint

        elif request_type.upper() == "POST" and params is not None:
            message = timestamp + "POST" + endpoint + json.dumps(params)

        data = self.sign(message)
        self.headers["OK-ACCESS-SIGN"] = data
        self.headers["OK-ACCESS-TIMESTAMP"] = timestamp

        self.url_payload = message  # saving payload sent to okx

    def _get(self, api_type: str, endpoint: str, params: Optional[Dict] = None):
        """
        get method - split by either public or private
        public does not require api keys
        private requires api keys

        Args:
            type (str): "public" vs "private
            endpoint (str): '/api/v5/account/balance?ccy=BTC' with params
            params (dict, optional): Defaults to None.
        """
        if api_type == "public":
            # no headers required
            try:
                response = requests.get(
                    self.okx_base_url + endpoint,
                    params=params,
                    timeout=self.timeout,
                )
            except Exception as error:
                print(f"public api call error: {error}")

        elif api_type == "private":
            try:
                self.hashing("GET", endpoint, params)
                response = requests.get(
                    self.okx_base_url + endpoint,
                    headers=self.headers,
                    params=params,
                    timeout=self.timeout,
                )
            except Exception as error:
                print(f"private api call error: {error}")
                print(f"printing url payload: {self.url_payload}")

        return response.json()

    def _post(self, api_type: str, endpoint: str, params: Optional[Dict]):
        """
        post method - split by either public or private
        public does not require api keys
        private requires api keys

        Args:
            type (str): "public" vs "private
            endpoint (str): '/api/v5/account/balance?ccy=BTC' with params
            params (dict, optional): Defaults to None.
        """
        if api_type == "public":
            # no headers required
            try:
                response = requests.post(
                    self.okx_base_url + endpoint,
                    json=params,
                    timeout=self.timeout,
                )
            except Exception as error:
                print(f"public api call error: {error}")

        elif api_type == "private":
            try:
                self.hashing("POST", endpoint, params)
                response = requests.post(
                    self.okx_base_url + endpoint,
                    headers=self.headers,
                    json=params,
                    timeout=self.timeout,
                )
            except Exception as error:
                print(f"private api call error: {error}")
                print(f"printing url payload: {self.url_payload}")

        return response.json()

    #######################
    ### trading account ###
    #######################

    # REST API for trading account

    def get_balance_trading(self, params: Optional[Dict] = None):
        """
        private method - GET
        Retrieve a list of assets (with non-zero balance),
        remaining balance, and available amount in the trading account.

        https://www.okx.com/docs-v5/en/#rest-api-account-get-balance

        Args:
            params (dict, optional): Defaults to None.

            Parameters 	Types 	Required 	Description
            ccy         String  No          single or multiple up to 20
                                            BTC or BTC,ETH...
        """
        api_type = "private"
        endpoint = "/api/v5/account/balance"
        data = self._get(api_type, endpoint, params)
        return data

    def get_positions_trading(self, params: Optional[Dict] = None):
        """
        private method - GET
        Retrieve information on your positions.
        When the account is in net mode, net positions will be displayed,
        and when the account is in long/short mode,
        long or short positions will be displayed.
        Return in reverse chronological order using ctime.

        https://www.okx.com/docs-v5/en/#rest-api-account-get-positions

        Args:
            params (dict, optional): Defaults to None.

            Parameters 	Types 	Required 	Description
            instType    String  No          MARGIN, SWAP, FUTURES, OPTION
            instId      String  No          BTC-USD-190927-5000-C
            posId       String  No
        """
        api_type = "private"
        endpoint = "/api/v5/account/positions"
        data = self._get(api_type, endpoint, params)
        return data

    def get_max_loan_by_instrument(self, params: dict):
        """
        private method - GET

        https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-the-maximum-loan-of-instrument

        Args:
            params (dict)

            Parameters 	Types 	Required 	Description
            instId      String  Yes         BTC-USDT,ETH-USDT
            mgnMode     String  Yes         isolated or cross
            mgnCcy      String  No
        """
        api_type = "private"
        endpoint = "/api/v5/account/max-loan"
        data = self._get(api_type, endpoint, params)
        return data

    def get_fees(self, params: dict):
        """
        private method - GET

        https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-fee-rates

        Args:
            params (dict)

            Parameters 	Types 	Required 	Description
            instType    String  Yes         SPOT, MARGIN ...
            instId      String  no          BTC-USDT,ETH-USDT
            uly         String  no          BTC-USD Applicable to FUTURES/SWAP/OPTION
            instFamily  String  Yes         BTC-USD Applicable to FUTURES/SWAP/OPTION
        """
        api_type = "private"
        endpoint = "/api/v5/account/trade-fee"
        data = self._get(api_type, endpoint, params)
        return data

    def get_interest_rate(self, params: dict):
        """
        private method - GET

        https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-interest-rate

        Args:
            params (dict)

            Parameters 	Types 	Required 	Description
            ccy         String  No          BTC
        """
        api_type = "private"
        endpoint = "/api/v5/account/interest-rate"
        data = self._get(api_type, endpoint, params)
        return data

    def get_borrow_interest_limit(self, params: Optional[Dict] = None):
        """
        private method - GET

        https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-borrow-interest-and-limit

        Args:
            params (dict)

            Parameters 	Types 	Required 	Description
            type        String  No          1 or 2. 1=VIP Loans, 2=Market Loans
            ccy         String  No          BTC
        """
        api_type = "private"
        endpoint = "/api/v5/account/interest-limits"
        data = self._get(api_type, endpoint, params)
        return data

    def get_fixed_loan_borrow_limit(self, params: Optional[Dict] = None):
        """
        private method - GET

        https://www.okx.com/docs-v5/en/#trading-account-rest-api-get-fixed-loan-borrow-limit
        """
        api_type = "private"
        endpoint = "/api/v5/account/fixed-loan/borrowing-limit"
        data = self._get(api_type, endpoint, params)
        return data

    ##########################
    ### order book trading ###
    ##########################

    ### order book trading > trade

    def place_order(self, params: dict):
        """
        private method - POST
        Placing order

        https://www.okx.com/docs-v5/en/#rest-api-trade-place-order

        Rate Limit: 60 requests per 2 seconds
        Rate Limit of leading contracts for Copy Trading: 1 requests per 2 seconds
        Rate limit rule (except Options): UserID + Instrument ID
        Rate limit rule (Options only): UserID + Instrument Family

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instId      String  Yes         instrument id e.g. BTC-USDT
            tdMode      String  Yes         Trade mode e.g. cash, cross, isolated
            clOrdId     String  No          client order ID - assigned by us
            tag         String  No          order tag
            side        String  Yes         buy or sell
            ordType     String  Yes         market, limit, post_only, fok, ioc
            sz          String  Yes         size - quantity to buy or sell
            px          String  Conditional only for limit, post_only, fok, ioc
        """
        api_type = "private"
        endpoint = "/api/v5/trade/order"
        data = self._post(api_type, endpoint, params)
        return data

    def cancel_order(self, params: dict):
        """
        private method - POST
        Cancel order

        https://www.okx.com/docs-v5/en/#order-book-trading-trade-post-cancel-order

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instId      String  Yes         instrument id e.g. BTC-USDT
            ordId       String  Conditional either ordId or clOrdId required
            clOrdId     String  Conditional either ordId or clOrdId required
        """
        api_type = "private"
        endpoint = "/api/v5/trade/cancel-order"
        data = self._post(api_type, endpoint, params)
        return data

    def get_order_details(self, params: dict):
        """
        private method - GET
        Retrieve order details

        https://www.okx.com/docs-v5/en/#order-book-trading-trade-get-order-details

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instId      String  Yes         instrument id e.g. BTC-USDT
            ordId       String  Conditional either ordId or clOrdId required
            clOrdId     String  Conditional either ordId or clOrdId required
        """
        api_type = "private"
        endpoint = "/api/v5/trade/order"
        data = self._get(api_type, endpoint, params)
        return data

    def get_order_list(self, params: Optional[Dict] = None):
        """
        private method - GET
        Retrieve all incomplete orders under the current account.

        https://www.okx.com/docs-v5/en/#order-book-trading-trade-get-order-list

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instType    Str     no          SPOT MARGIN SWAP FUTURES OPTION
            uly         Str     no          underlying
            instId      Str     no          BTC-USDT
            ordType     Str     no          market limit post_only ...
            state       Str     no          live partially_filled
            after       Str     no          pull records earlier than requested ordId
            before      Str     no          pull records newer than requested ordId
            limit       Str     no          default 100, max 100
        """
        api_type = "private"
        endpoint = "/api/v5/trade/orders-pending"
        data = self._get(api_type, endpoint, params)
        return data

    def get_transaction_details_3d(self, params: Optional[Dict] = None):
        """
        private method - GET
        Retrieve recently-filled transaction details in the last 3 days.
        can have multiple fills per order id

        https://www.okx.com/docs-v5/en/#order-book-trading-trade-get-transaction-details-last-3-days

        Args:
            params (dict, optional): Defaults to None.

            Parameters 	Types 	Required 	Description
            instType    String  No          SPOT, MARGIN, SWAP, FUTURES, OPTION
            uly         String  No          applicable to FUTURES/SWAP/OPTION
            instFamily  String  No          applicable to FUTURES/SWAP/OPTION
            instId      String  No          BTC-USD-190927-5000-C
            ordId       String  No          Order ID
            after       String  No          Pagination of data to return records earlier than the requested billId
            before      String  No          Pagination of data to return records newer than the requested billId
            begin       String  No          begin timestamp e.g. 1597026383085
            end         String  No          end timestamp e.g. 1597026383085
            limit       String  No          max = 100, default = 100
        """
        api_type = "private"
        endpoint = "/api/v5/trade/fills"
        data = self._get(api_type, endpoint, params)
        return data

    def get_transaction_details_3m(self, params: dict):
        """
        private method - GET
        Retrieve recently-filled transaction details in the last 3 months.

        https://www.okx.com/docs-v5/en/#order-book-trading-trade-get-transaction-details-last-3-months

        Args:
            params (dict, optional): Defaults to None.

            Parameters 	Types 	Required 	Description
            instType    String  Yes         SPOT, MARGIN, SWAP, FUTURES, OPTION
            uly         String  No          applicable to FUTURES/SWAP/OPTION
            instFamily  String  No          applicable to FUTURES/SWAP/OPTION
            instId      String  No          BTC-USD-190927-5000-C
            ordId       String  No          Order ID
            after       String  No          Pagination of data to return records earlier than the requested billId
            before      String  No          Pagination of data to return records newer than the requested billId
            begin       String  No          begin timestamp e.g. 1597026383085
            end         String  No          end timestamp e.g. 1597026383085
            limit       String  No          max = 100, default = 100
        """
        api_type = "private"
        endpoint = "/api/v5/trade/fills-history"
        data = self._get(api_type, endpoint, params)
        return data

    def post_transaction_details_2y(self, params: dict):
        """Apply for recently-filled transaction details
        in the past 2 years except for last 3 months.

        Args:
            params (dict): _description_

            Parameters 	Types 	Required 	Description
            year        String  Yes         2023
            quarter     String  Yes         Q1, Q2...
        """
        api_type = "private"
        endpoint = "/api/v5/trade/fills-archive"
        data = self._post(api_type, endpoint, params)
        return data

    def get_transaction_details_2y(self, params: dict):
        """Retrieve recently-filled transaction details
        in the past 2 years except for last 3 months.

        need send post request first

        Args:
            params (dict): _description_

            Parameters 	Types 	Required 	Description
            year        String  Yes         2023
            quarter     String  Yes         Q1, Q2...
        """
        api_type = "private"
        endpoint = "/api/v5/trade/fills-archive"
        data = self._get(api_type, endpoint, params)
        return data

    ### market data ###
    def get_tickers(self, params: dict):
        """
        public method - GET
        Retrieve the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.
        https://www.okx.com/docs-v5/en/?python#order-book-trading-market-data-get-tickers

        Args:
            Parameter 	Type 	Required 	Description
            instType 	String 	Yes 	    SPOT, SWAP, FUTURES, OPTION
            uly         String  No          e.g. BTC-USD applicable to FUTURES/SWAP/OPTION
            instFamily  String  No          applicable to FUTURES/SWAP/OPTION
        """
        api_type = "public"
        endpoint = "/api/v5/market/tickers"
        data = self._get(api_type, endpoint, params)
        return data

    def get_ticker(self, params: dict):
        """
        public method - GET
        Order Book Trading > Market Data > Get / Ticker
        Retrieve the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours.
        https://www.okx.com/docs-v5/en/?python#order-book-trading-market-data-get-ticker

        Args:
            Parameter 	Type 	Required 	Description
            instId 	    String 	Yes 	    Instrument ID, e.g. BTC-USD-SWAP
        """
        api_type = "public"
        endpoint = "/api/v5/market/ticker"
        data = self._get(api_type, endpoint, params)
        return data

    def get_orderbook(self, params: dict):
        """
        public method - GET
        Retrieve order book of the instrument.
        https://www.okx.com/docs-v5/en/?python#order-book-trading-market-data-get-order-book

        Args:
            Parameter 	Type 	Required 	Description
            instId 	    String 	Yes 	    Instrument ID, e.g. BTC-USDT
            sz          String  No          Orderbook depth, max 400, default 1
        """
        api_type = "public"
        endpoint = "/api/v5/market/books"
        data = self._get(api_type, endpoint, params)
        return data

    def get_candlesticks_history(self, params: dict):
        """
        public method - GET
        Retrieve history candlestick charts from recent years
        (It is last 3 months supported for 1s candlestick).
        Charts are returned in groups based on the requested bar.
        https://www.okx.com/docs-v5/en/#order-book-trading-market-data-get-candlesticks-history

        Args:
            Parameter 	Type 	Required 	Description
            instId 	    String 	Yes 	    Instrument ID, e.g. BTC-USDT
            bar         String  No          default = "1m" e.g. [1m/3m/5m/15m/30m/1H/2H/4H]
            after       String  No          ts # records earlier than specified time
            before      String  No          ts # records after specified time
            limit       String  No          max is 300, default is 100
        """
        api_type = "public"
        endpoint = "/api/v5/market/history-candles"
        data = self._get(api_type, endpoint, params)
        return data

    ###################
    ### public data ###
    ###################

    def get_instruments(self, params: dict):
        """
        public method - GET
        Retrieve a list of instruments with open contracts.
        https://www.okx.com/docs-v5/en/?python#public-data-rest-api-get-instruments

        Args:
            Parameter 	Type 	Required 	Description
            instType 	String 	Yes 	    Instrument type: SPOT,MARGIN,SWAP,FUTURES,OPTIONS
            uly         String  Conditional
        """
        api_type = "public"
        endpoint = "/api/v5/public/instruments"
        return self._get(api_type, endpoint, params)

    #######################
    ### funding account ###
    #######################

    # funding methods
    def get_currencies(self, params: dict = None):
        """
        private method - GET
        Retrieve a list of all currencies.
        https://www.okx.com/docs-v5/en/?python#funding-account-rest-api-get-currencies

        Args:
            Parameter 	Type 	Required 	Description
            ccy         String  No          BTC or BTC,ETH,... (max 20)
        """
        api_type = "private"
        endpoint = "/api/v5/asset/currencies"
        return self._get(api_type, endpoint, params)

    def get_balance_funding(self, params: dict = None):
        """Get balance in funding account
        https://www.okx.com/docs-v5/en/#rest-api-funding-get-balance
        """
        api_type = "private"
        endpoint = "/api/v5/asset/balances"
        return self._get(api_type, endpoint, params)
