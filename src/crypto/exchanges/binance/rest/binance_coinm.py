"""
Coin Margined APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

import requests

from python.crypto.exchanges.binance.rest.binance_client import Binance


class BinanceCoinm(Binance):
    """
    CoinMargined APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.binance_coinm_base_url = "https://dapi.binance.com"
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
        https://binance-docs.github.io/apidocs/delivery/en/#order-book

        orderbook data

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     yes         BTCUSD_PERP
            limit   int     no          default=500 valid=[5,10,20,50,100,500,1000]
        """
        endpoint = "/dapi/v1/depth"
        response = requests.get(
            self.binance_coinm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    def get_kline(self, params: dict) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/delivery/en/#kline-candlestick-data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            interval 	ENUM 	YES
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	        Default 500; max 1000.
        """
        endpoint = "/dapi/v1/klines"
        response = requests.get(
            self.binance_coinm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    def get_symbol_price_ticker_v2(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/delivery/en/#symbol-price-ticker

        Latest price for a symbol or symbols.

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     no          BTCUSD_200626
        """
        endpoint = "/dapi/v1/ticker/price"
        response = requests.get(
            self.binance_coinm_base_url + endpoint, params, timeout=self.timeout
        )
        return response.json()

    #####################
    ### coinm methods ###
    #####################

    def post_new_order(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade

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
        endpoint = "/dapi/v1/order"
        url = self.signed_request_url(self.binance_coinm_base_url, endpoint, params)
        return self._post(url)

    def get_query_order(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/delivery/en/#query-order-user_data

        Check an order's status.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            origClientOrderId	STRING	    NO
        """
        endpoint = "/dapi/v1/order"
        url = self.signed_request_url(self.binance_coinm_base_url, endpoint, params)
        return self._get(url)

    def get_coinm_account_balance(self) -> dict:
        """
        Public
        GET method
        https://binance-docs.github.io/apidocs/delivery/en/#futures-account-balance-user_data
        """
        endpoint = "/dapi/v1/balance"
        url = self.signed_request_url(self.binance_coinm_base_url, endpoint)
        return self._get(url)
