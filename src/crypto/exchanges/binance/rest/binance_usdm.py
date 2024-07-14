"""
USD Margined APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

from crypto.exchanges.binance.rest.binance_client import Binance


class BinanceUsdm(Binance):
    """
    USDMargined APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.binance_usdm_base_url = "https://fapi.binance.com"

    #############################
    ### market data endpoints ###
    #############################

    def get_usdm_orderbook(self, params: dict) -> dict:
        """
        PUBLIC GET method
        https://binance-docs.github.io/apidocs/futures/en/#order-book

        orderbook data

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     yes
            limit   int     no          default=500 valid=[5,10,20,50,100,500,1000]
        """
        endpoint = "/fapi/v1/depth"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_usdm_base_url, endpoint, params
        )

    def get_usdm_kline(self, params: dict) -> dict:
        """
        PUBLIC GET request
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
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_usdm_base_url, endpoint, params
        )

    def get_usdm_price_ticker_v2(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker-v2

        Latest price for a symbol or symbols.

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     no
        """
        endpoint = "/fapi/v2/ticker/price"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_usdm_base_url, endpoint, params
        )

    ###############################
    ### Account/Trades Endpoint ###
    ###############################

    def post_usdm_order(self, params: dict) -> dict:
        """
        PRIVATE POST request
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
        return self.rest_requests(
            "PRIVATE", "POST", self.binance_usdm_base_url, endpoint, params
        )

    def get_usdm_order(self, params: dict) -> dict:
        """
        PRIVATE GET request
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
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_usdm_base_url, endpoint, params
        )

    def delete_usdm_order(self, params: dict) -> dict:
        """
        PRIVATE DELETE request
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
        return self.rest_requests(
            "PRIVATE", "DELETE", self.binance_usdm_base_url, endpoint, params
        )

    def get_usdm_orders(self, params: dict) -> dict:
        """
        Private GET request
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
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_usdm_base_url, endpoint, params
        )

    def get_usdm_account_balance(self) -> dict:
        """
        Private GET request
        https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-v2-user_data

        Gets USDM account balances
        """
        endpoint = "/fapi/v2/balance"
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_usdm_base_url, endpoint
        )

    def get_usdm_trade_list(self, params: dict) -> dict:
        """
        Private GET request
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
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_usdm_base_url, endpoint, params
        )
