"""
Coin Margined APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

from crypto.exchanges.binance.rest.binance_client import Binance


class BinanceCoinm(Binance):
    """
    CoinMargined APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.binance_coinm_base_url = "https://dapi.binance.com"
        self.timeout = 5

    #############################
    ### market data endpoints ###
    #############################

    def get_coinm_exchange_info(self) -> dict:
        """
        PUBLIC GET method
        https://binance-docs.github.io/apidocs/delivery/en/#exchange-information

        Current exchange trading rules and symbol information
        """
        endpoint = "/dapi/v1/exchangeInfo"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_coinm_base_url, endpoint
        )

    def get_coinm_orderbook(self, params: dict) -> dict:
        """
        PUBLIC GET method
        https://binance-docs.github.io/apidocs/delivery/en/#order-book

        orderbook data

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     yes         BTCUSD_PERP
            limit   int     no          default=500 valid=[5,10,20,50,100,500,1000]
        """
        endpoint = "/dapi/v1/depth"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_coinm_base_url, endpoint, params
        )
    
    def get_coinm_funding_rate(self, params: dict) -> dict:
        """
        PUBLIC GET method
        https://binance-docs.github.io/apidocs/delivery/en/#get-funding-rate-history-of-perpetual-futures

        coinm perp funding rates

        Args:
            params (dict):
            NAME        TYPE    MANDATORY   DESCRIPTION
            symbol      str     yes         BTCUSD_PERP
            startTime   long    no          time in ms inclusive
            endTime     long    no          time in ms inclusive
            limit       int     no          default=500 valid=[5,10,20,50,100,500,1000]
        """
        endpoint = "/dapi/v1/fundingRate"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_coinm_base_url, endpoint, params

    def get_coinm_kline(self, params: dict) -> dict:
        """
        PUBLIC GET request
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
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_coinm_base_url, endpoint, params
        )

    def get_coinm_symbol_price_ticker(self, params: Optional[Dict] = None) -> dict:
        """
        PUBLIC GET request
        https://binance-docs.github.io/apidocs/delivery/en/#symbol-price-ticker

        Latest price for a symbol or symbols.

        Args:
            params (dict):
            NAME    TYPE    MANDATORY   DESCRIPTION
            symbol  str     no          BTCUSD_200626
        """
        endpoint = "/dapi/v1/ticker/price"
        return self.rest_requests(
            "PUBLIC", "GET", self.binance_coinm_base_url, endpoint, params
        )

    #####################
    ### coinm methods ###
    #####################

    def post_coinm_order(self, params: dict) -> dict:
        """
        PRIVATE POST request
        https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade

        Send in a new order.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol              str         yes
            side                enum        yes         "BUY" or "SELL"
            type                enum        yes         "LIMIT", "MARKET"
            timeInForce         enum        no          "GTC", "FOK", "IOC"
            quantity            decimal     no          number of contracts
            reduceOnly          str         no
            price               decimal     no
            newClientOrderId    str         no          unique id among open orders
        """
        endpoint = "/dapi/v1/order"
        return self.rest_requests(
            "PRIVATE", "POST", self.binance_coinm_base_url, endpoint, params
        )

    def get_coinm_order(self, params: dict) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/delivery/en/#query-order-user_data

        Check an order's status.

        These orders will not be found:
            order status is CANCELED or EXPIRED, AND
            order has NO filled trade, AND
            created time + 3 days < current time

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            origClientOrderId	STRING	    NO
        """
        endpoint = "/dapi/v1/order"
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_coinm_base_url, endpoint, params
        )

    def delete_coinm_order(self, params: dict) -> dict:
        """
        PRIVATE DELETE request
        https://binance-docs.github.io/apidocs/delivery/en/#cancel-order-trade

        Cancel an active order.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
            orderId	            LONG	    NO
            origClientOrderId	STRING	    NO
        """
        endpoint = "/dapi/v1/order"
        return self.rest_requests(
            "PRIVATE", "DELETE", self.binance_coinm_base_url, endpoint, params
        )

    def delete_coinm_all_orders(self, params: dict) -> dict:
        """
        PRIVATE DELETE request
        https://binance-docs.github.io/apidocs/delivery/en/#cancel-all-open-orders-trade

        Cancel an active order.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    YES
        """
        endpoint = "/dapi/v1/allOpenOrders"
        return self.rest_requests(
            "PRIVATE", "DELETE", self.binance_coinm_base_url, endpoint, params
        )

    def get_coinm_open_orders(self, params: dict) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/delivery/en/#current-all-open-orders-user_data

        Get all open orders on a symbol. Careful when accessing this with no symbol.

        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    NO
            pair                STRING      NO
        """
        endpoint = "/dapi/v1/openOrders"
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_coinm_base_url, endpoint, params
        )

    def get_coinm_account_balance(self) -> dict:
        """
        PRIVATE GET method
        https://binance-docs.github.io/apidocs/delivery/en/#futures-account-balance-user_data
        """
        endpoint = "/dapi/v1/balance"
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_coinm_base_url, endpoint
        )

    def get_coinm_trade_list(self, params: dict) -> dict:
        """
        PRIVATE GET method
        https://binance-docs.github.io/apidocs/delivery/en/#account-trade-list-user_data

        Get trades for a specific account and symbol.

        Either symbol or pair must be sent
        Args:
            params (dict):
            NAME                TYPE        MANDATORY   DESCRIPTION
            symbol	            STRING	    NO
            pair                STRING      NO
            orderId             STRING      NO
            startTime           LONG        NO
            endTime             LONG        NO
            fromId              LONG        NO          Trade id to fetch from.
                                                        Default gets most recent trades.
            limit               INT         NO          Default 50; max 1000
        """
        endpoint = "/dapi/v1/userTrades"
        return self.rest_requests(
            "PRIVATE", "GET", self.binance_coinm_base_url, endpoint, params
        )
