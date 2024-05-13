"""
USD Margined APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

import requests

from python.crypto.exchanges.binance.rest.binance_client import Binance


class BinanceUsdm(Binance):
    """
    USDMargined APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.binance_usdm_base_url = "https://fapi.binance.com"
        self.timeout = 5

    #########################
    ### Standard Requests ###
    #########################

    def _get(self, url: str):
        """
        GET Requests
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as e:
            print(e)

    def _post(self, url: str):
        """
        POST Requests
        """
        try:
            response = requests.post(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as e:
            print(e)

    def _delete(self, url: str):
        """
        DELETE Request
        """
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as e:
            print(e)

    #############################
    ### market data endpoints ###
    #############################

    def get_orderbook(self, params: dict) -> dict:
        """
        Public
        GET method
        https://binance-docs.github.io/apidocs/futures/en/#order-book

        orderbook data

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     yes
            limit   int     no          default=500 valid=[5,10,20,50,100,500,1000]
        """
        endpoint = "/fapi/v1/depth"
        response = requests.get(
            self.binance_usdm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    def get_kline(self, params: dict) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            interval 	ENUM 	YES
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	        Default 500; max 1000.
        """
        endpoint = "/fapi/v1/klines"
        response = requests.get(
            self.binance_usdm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    def get_symbol_price_ticker_v2(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker

        Latest price for a symbol or symbols.

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     no
        """
        endpoint = "/fapi/v2/ticker/price"
        response = requests.get(
            self.binance_usdm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    ###############################
    ### Account/Trades Endpoint ###
    ###############################

    def post_new_order(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/futures/en/#new-order-trade

        Send in a new order.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol              str         yes
            side                enum        yes         "BUY" or "SELL"
            type                enum        yes         "LIMIT", "MARKET"
            timeInForce         enum        no          "GTC", "FOK", "IOC"
            quantity            decimal     no
            reduceOnly          str         no
            price               decimal     no
            newClientOrderId    str         no          unique id among open orders
        """
        endpoint = "/fapi/v1/order"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint, params)
        return self._post(url)

    def get_query_order(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data

        Check an order's status.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            origClientOrderId	STRING	    NO
        """
        endpoint = "/fapi/v1/order"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint, params)
        return self._get(url)

    def delte_order(self, params: dict) -> dict:
        """
        PRIVATE
        DELETE request
        https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade

        Cancel an active order.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            origClientOrderId	STRING	    NO
        """
        endpoint = "/fapi/v1/order"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint, params)
        return self._delete(url)

    def get_all_orders(self, params: dict) -> dict:
        """
        Private
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#all-orders-user_data

        Gets all account orders; active, canceled, or filled.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            startTime           Long        No
            endTime             Long        No
            limit               INT         No          Default 500, Max 1000
        """
        endpoint = "/fapi/v1/allOrders"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint, params)
        return self._get(url)

    def get_account_balance(self) -> dict:
        """
        Private
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-v2-user_data

        Gets USDM account balances
        """
        endpoint = "/fapi/v2/balance"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint)
        return self._get(url)

    def get_account_trade_list(self, params: dict) -> dict:
        """
        Private
        GET request
        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data

        Get trades for a specific account and symbol.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            startTime           Long        No
            endTime             Long        No
            limit               INT         No          Default 500, Max 1000
        """
        endpoint = "/fapi/v1/userTrades"
        url = self.signed_request_url(self.binance_usdm_base_url, endpoint, params)
        return self._get(url)
