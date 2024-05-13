"""
Spot APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

import requests

from src.crypto.exchanges.binance.rest.binance_client import Binance


class BinanceIsolatedMargin(Binance):
    """
    Spot APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.spot_margin_url = "https://api.binance.com"
        self.timeout = 3

    ########################################################
    ### adding exceptions to sending get / post requests ###
    ########################################################

    def send_get_request(self, url: str):
        """
        sending authenticated get requests
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as error:
            print(error)

    def send_post_request(self, url: str):
        """
        sending authenticated post requests
        """
        try:
            response = requests.post(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as error:
            print(error)

    def send_delete_request(self, url: str):
        """
        sending authenticated delete requests
        """
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as error:
            print(error)

    ######################
    ### spot endpoints ###
    ######################

    def get_exchange_infomation(self, symbol: str = None) -> dict:
        """
        public request
        https://binance-docs.github.io/apidocs/spot/en/#exchange-information
        Current exchange trading rules and symbol information

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES         "BTCUSDT"
            symbols     STRING 	YES         ["BTCUSDT","BNBUSDT"] either symbol or symbols
        """
        if symbol:
            response = requests.get(
                self.spot_margin_url + "/api/v3/exchangeInfo",
                params={"symbol": symbol},
                timeout=self.timeout,
            )
        else:
            response = requests.get(
                self.spot_margin_url + "/api/v3/exchangeInfo",
                timeout=self.timeout,
            )

        data = response.json()
        return data

    def get_symbol_price_ticker(self, params: dict) -> dict:
        # public request
        # https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES         "BTCUSDT"
            symbols     STRING 	YES         ["BTCUSDT","BNBUSDT"] either symbol or symbols
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/ticker/price", params, timeout=self.timeout
        )
        data = response.json()
        return data

    #######################
    ### isolated margin ###
    #######################

    # borrow and repay
    def post_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        private POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-repay-margin
        Margin account borrow/repay(MARGIN)
        Cross + Isolated

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	YES         "BTC"
            isIsolated  STRING  YES         True for isolated, False for cross
            symbol      STRING  YES         only for isolated margin
            amount      STRING  YES
            type        STRING  YES         BORROW or REPAY
        """
        url_endpoint = "/sapi/v1/margin/borrow-repay"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_post_request(url)

    def get_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-borrow-repay-records-in-margin-account-user_data
        Query borrow/repay records in Margin account
        Cross + Isolated

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING  NO          "BTC"
            isisolated  STRING  NO          TRUE for isolated, FALSE for cross
            txid        LONG    NO          tranId in POST /sapi/v1/margin/loan
            startTime   LONG    NO
            endTime     LONG    NO
            current     LONG    NO          Current querying page. Start from 1. Default:1
            size        LONG    NO          Default: 10 Max: 100
            type        STRING  YES         BORROW or REPAY
        """
        url_endpoint = "/sapi/v1/margin/borrow-repay"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_post_request(url)

    # placing orders
    def get_orderbook(self, params: dict) -> dict:
        """
        public GET request
        https://binance-docs.github.io/apidocs/spot/en/#order-book
        same orderbook as for spot
        Args:
            params (dict):
            Name    Type    Mandatory   Description
            symbol 	STRING 	YES
            limit 	INT 	NO 	Default 100; max 5000.
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/depth", params, timeout=self.timeout
        )
        return response.json()

    def post_margin_new_order(self, params: dict) -> dict:
        """
        private POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade
        Post a new order for margin account.
        Cross + Isolated

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            symbol 	            STRING 	    YES
            isIsolated 	        TRING 	    NO 	        True or False
            side 	            ENUM 	    YES 	    BUY or SELL
            type 	            ENUM 	    YES
            quantity 	        DECIMAL 	NO
            quoteOrderQty 	    DECIMAL 	NO
            price 	            DECIMAL 	NO
            stopPrice 	        DECIMAL 	NO
            newClientOrderId 	STRING 	    NO 	Automatically generated if not sent.
            icebergQty 	        DECIMAL 	NO
            newOrderRespType 	ENUM 	    NO
            sideEffectType 	    ENUM 	    NO
            timeInForce 	    ENUM 	    NO 	GTC,IOC,FOK
            recvWindow 	        LONG 	    NO 	The value cannot be greater than 60000
            timestamp 	        LONG 	    YES
        """
        url_endpoint = "/sapi/v1/margin/order"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_post_request(url)

    def delete_margin_cancel_order(self, params: dict) -> dict:
        """
        private DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade
        Cancel an active order for margin account.
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated 	        STRING 	NO 	        TRUE or FALSE
            orderId 	        LONG 	NO
            origClientOrderId 	STRING 	NO
            newClientOrderId 	STRING 	NO
            recvWindow 	        LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	        LONG 	YES
        """
        url_endpoint = "/sapi/v1/margin/order"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_delete_request(url)

    def get_interest_history(self, params: Optional[Dict] = None) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data
        Gets interest history
        Cross + Isolated

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            asset 	        STRING 	NO
            isolatedSymbol 	STRING 	NO 	        isolated symbol
                                                If isolatedSymbol is not sent,
                                                crossed margin data will be returned
            startTime 	    LONG 	NO
            endTime 	    LONG 	NO
            current 	    LONG 	NO 	        Currently querying page. Start from 1. Default:1
            size 	        LONG 	NO 	        Default:10 Max:100
            recvWindow 	    LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	    LONG 	YES
        """
        url_endpoint = "/sapi/v1/margin/interestHistory"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_margin_account_order(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-order-user_data
        Gets single order info - either orderId or origClientOrderId required
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
            orderId             LONG    NO
            origClientOrderId   STRING  NO
        """
        url_endpoint = "/sapi/v1/margin/order"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_margin_account_open_orders(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-orders-user_data
        Gets all open orders
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
        """
        url_endpoint = "/sapi/v1/margin/openOrders"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_margin_account_all_orders(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-orders-user_data
        Gets historical orders
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
            orderId             LONG    NO
            startTime           LONG    NO
            endTime             LONG    NO
            limit               INT     NO          Default 500, max 500
        """
        url_endpoint = "/sapi/v1/margin/allOrders"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_margin_account_trades(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data
        Gets historical margin trades
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
            orderId             LONG    NO
            startTime           LONG    NO
            endTime             LONG    NO
            fromId              LONG    NO          TradeId to fetch from
            limit               INT     NO          Default 500, max 500
        """
        url_endpoint = "/sapi/v1/margin/myTrades"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_isolated_margin_info(self) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data
        Gets balances for isolated margin account
        Isolated only

        borrowed
        free
        interest
        locked
        netasset -> can be negative
        """
        url_endpoint = "/sapi/v1/margin/isolated/account"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint)
        return self.send_get_request(url)

    #######################
    ### toggle bnb burn ###
    #######################

    def post_toggle_bnb_burn(self, params: dict) -> dict:
        """
        private POST request
        https://binance-docs.github.io/apidocs/spot/en/#toggle-bnb-burn-on-spot-trade-and-margin-interest-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            spotBNBBurn     STRING 	NO          "true" or "false"
            interestBNBBurn STRING 	NO 		    "true" or "false"
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
        """
        url_endpoint = "/sapi/v1/bnbBurn"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_post_request(url)

    def get_bnb_burn_status(self, params: Optional[Dict] = None) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
        """
        url_endpoint = "/sapi/v1/bnbBurn"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    ######################
    ### post transfers ###
    ######################

    def get_api_key_permission(self) -> dict:
        """Gets permissions set for api key"""
        url_endpoint = "/sapi/v1/account/apiRestrictions"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint)
        return self.send_get_request(url)

    def post_universal_transfer(self, params: dict) -> dict:
        """
        private POST request
        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer-user_data

        fromSymbol must be sent when type are ISOLATEDMARGIN_MARGIN and ISOLATEDMARGIN_ISOLATEDMARGIN
        toSymbol must be sent when type are MARGIN_ISOLATEDMARGIN and ISOLATEDMARGIN_ISOLATEDMARGIN

        type:
        MAIN_MARGIN - Spot account transfer to Margin（cross）account
        MARGIN_MAIN - Margin（cross）account transfer to Spot account

        MAIN_ISOLATED_MARGIN Spot account transfer to Isolated margin account
        ISOLATED_MARGIN_MAIN Isolated margin account transfer to Spot account

        MAIN_UMFUTURE Spot account transfer to USDⓈ-M Futures account
        UMFUTURE_MAIN USDⓈ-M Futures account transfer to Spot account

        Args:
            params (dict):
            Name            Type        Mandatory   Description
            type	        ENUM        YES
            asset           STRING      YES
            amount          DECIMAL     YES
            fromSymbol      STRING      NO
            toSymbol        STRING      NO
            recvWindow 	    LONG 	    NO
            timestamp 	    LONG 	    YES
        """
        url_endpoint = "/sapi/v1/asset/transfer"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_post_request(url)

    ########################
    ### Get Capital Flow ###
    ########################

    def get_capital_flow(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-cross-or-isolated-margin-capital-flow-user_data

        TRANSFER("Transfer")
        BORROW("Borrow")
        REPAY("Repay")
        BUY_INCOME("Buy-Trading Income")
        BUY_EXPENSE("Buy-Trading Expense")
        SELL_INCOME("Sell-Trading Income")
        SELL_EXPENSE("Sell-Trading Expense")
        TRADING_COMMISSION("Trading Commission")
        BUY_LIQUIDATION("Buy by Liquidation")
        SELL_LIQUIDATION("Sell by Liquidation")
        REPAY_LIQUIDATION("Repay by Liquidation")
        OTHER_LIQUIDATION("Other Liquidation")
        LIQUIDATION_FEE("Liquidation Fee")
        SMALL_BALANCE_CONVERT("Small Balance Convert")
        COMMISSION_RETURN("Commission Return")
        SMALL_CONVERT("Small Convert")

        Args:
            params (dict):
            Name            Type        Mandatory   Description
            asset           STRING      NO
            symbol          STRING      NO          Required for isolated margin
            type	        ENUM        YES         Refer above
            startTime       LONG        NO
            endTime         LONG        NO
            fromId          LONG        NO
            limit           LONG        NO
            recvWindow 	    LONG 	    NO
            timestamp 	    LONG 	    YES
        """
        url_endpoint = "/sapi/v1/margin/capital-flow"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)

    def get_max_borrow_amt(self, params: dict) -> dict:
        """
        private GET method
        https://binance-docs.github.io/apidocs/spot/en/#query-max-borrow-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            asset	        STRING	YES
            isolatedSymbol	STRING	NO	        isolated symbol
            recvWindow	    LONG	NO	        The value cannot be greater than 60000
            timestamp	    LONG	YES
        """
        url_endpoint = "/sapi/v1/margin/maxBorrowable"
        url = self.signed_request_url(self.spot_margin_url, url_endpoint, params)
        return self.send_get_request(url)
