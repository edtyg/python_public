"""
Spot APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log

transfer funds into cross margin account

can place normal orders if you have balances in margin account
i.e sell btc/usdt if you have btc
to buy btc/usdt if you have usdt

otherwise would need to place orders with margin buy (borrow) in params
"""

from typing import Dict, Optional

from crypto.exchanges.binance.rest.binance_client import Binance


class BinanceCrossMargin(Binance):
    """
    Spot APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.spot_margin_url = "https://api.binance.com"

    ######################
    ### spot endpoints ###
    ######################

    def get_exchange_information(self, params: dict) -> dict:
        """
        PUBLIC GET request
        https://binance-docs.github.io/apidocs/spot/en/#exchange-information
        Current exchange trading rules and symbol information

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES         "BTCUSDT"
            symbols     STRING 	YES         ["BTCUSDT","BNBUSDT"] either symbol or symbols
        """
        endpoint = "/api/v3/exchangeInfo"
        return self.rest_requests(
            "PUBLIC", "GET", self.spot_margin_url, endpoint, params
        )

    def get_symbol_price_ticker(self, params: dict) -> dict:
        """
        PUBLIC GET request
        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES         "BTCUSDT"
            symbols     STRING 	YES         ["BTCUSDT","BNBUSDT"] either symbol or symbols
        """
        endpoint = "/api/v3/ticker/price"
        return self.rest_requests(
            "PUBLIC", "GET", self.spot_margin_url, endpoint, params
        )

    ####################
    ### cross margin ###
    ####################

    def post_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        PRIVATE POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-repay-margin

        Margin account borrow/repay(MARGIN)
        Cross + Isolated

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	YES         "BTC"
            isisolated  STRING  YES         True for isolated, False for cross
            symbol      STRING  YES         only for isolated margin
            amount      STRING  YES
            type        STRING  YES         BORROW or REPAY
        """
        endpoint = "/sapi/v1/margin/borrow-repay"
        return self.rest_requests(
            "PRIVATE", "POST", self.spot_margin_url, endpoint, params
        )

    def get_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-borrow-repay-records-in-margin-account-user_data

        Query borrow/repay records in Margin account
        Cross + Isolated

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING  NO          "BTC"
            isisolated  STRING  NO          True for isolated, False for cross
            txid        LONG    NO          tranId in POST /sapi/v1/margin/loan
            startTime   LONG    NO
            endTime     LONG    NO
            current     LONG    NO          Current querying page. Start from 1. Default:1
            size        LONG    NO          Default: 10 Max: 100
            type        STRING  YES         BORROW or REPAY
        """
        endpoint = "/sapi/v1/margin/borrow-repay"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    def get_orderbook(self, params: dict) -> dict:
        """
        PUBLIC GET request
        https://binance-docs.github.io/apidocs/spot/en/#order-book

        same orderbook as for spot

        Args:
            params (dict):
            Name    Type    Mandatory   Description
            symbol 	STRING 	YES
            limit 	INT 	NO 	Default 100; max 5000.
        """
        endpoint = "/api/v3/depth"
        return self.rest_requests(
            "PUBLIC", "GET", self.spot_margin_url, endpoint, params
        )

    def post_margin_new_order(self, params: dict) -> dict:
        """
        PRIVATE POST request
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
        endpoint = "/sapi/v1/margin/order"
        return self.rest_requests(
            "PRIVATE", "POST", self.spot_margin_url, endpoint, params
        )

    def delete_margin_cancel_order(self, params: dict) -> dict:
        """
        PRIVATE DELETE request
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
        endpoint = "/sapi/v1/margin/order"
        return self.rest_requests(
            "PRIVATE", "DELETE", self.spot_margin_url, endpoint, params
        )

    def get_interest_history(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE GET request
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
        endpoint = "/sapi/v1/margin/interestHistory"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    # use this to get balances for cross margin account
    def get_cross_margin_details(self) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-account-details-user_data

        Get cross margin account details and balances
        """
        endpoint = "/sapi/v1/margin/account"
        return self.rest_requests("PRIVATE", "GET", self.spot_margin_url, endpoint)

    def get_margin_account_order(self, params: dict) -> dict:
        """
        PRIVATE GET request
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
        endpoint = "/sapi/v1/margin/order"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    def get_margin_account_open_orders(self, params: dict) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-orders-user_data

        Gets all open orders
        Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
        """
        endpoint = "/sapi/v1/margin/openOrders"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    def get_margin_account_all_orders(self, params: dict) -> dict:
        """
        PRIVATE GET request
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
        endpoint = "/sapi/v1/margin/allOrders"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    def get_margin_account_trades(self, params: dict) -> dict:
        """
        PRIVATE GET request
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
        endpoint = "/sapi/v1/margin/myTrades"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    #######################
    ### toggle bnb burn ###
    #######################

    def post_toggle_bnb_burn(self, params: dict) -> dict:
        """
        PRIVATE POST request
        https://binance-docs.github.io/apidocs/spot/en/#toggle-bnb-burn-on-spot-trade-and-margin-interest-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            spotBNBBurn     STRING 	NO          "true" or "false"
            interestBNBBurn STRING 	NO 		    "true" or "false"
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
        """
        endpoint = "/sapi/v1/bnbBurn"
        return self.rest_requests(
            "PRIVATE", "POST", self.spot_margin_url, endpoint, params
        )

    def get_bnb_burn_status(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
        """
        endpoint = "/sapi/v1/bnbBurn"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    ######################
    ### post transfers ###
    ######################

    def post_universal_transfer(self, params: dict) -> dict:
        """
        PRIVATE POST request
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
        endpoint = "/sapi/v1/asset/transfer"
        return self.rest_requests(
            "PRIVATE", "POST", self.spot_margin_url, endpoint, params
        )

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
        COMMISSION_RETURN("Commission Return") # fee return history
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
        endpoint = "/sapi/v1/margin/capital-flow"
        return self.rest_requests(
            "PRIVATE", "GET", self.spot_margin_url, endpoint, params
        )

    #################
    ### Websocket ###
    #################

    def post_create_listen_key(self):
        """
        PRIVATE POST request
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        Creates a websocket listen key for authenticated connections
        """
        endpoint = "/sapi/v1/userDataStream"
        return self.rest_requests("PRIVATE", "POST", self.spot_margin_url, endpoint)

    def put_listen_key(self):
        """
        PRIVATE PUT request
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        Creates a websocket listen key for authenticated connections
        valid for 60 mins
        doing a put request will extend by 60 mins
        """
        endpoint = "/sapi/v1/userDataStream"
        return self.rest_requests("PRIVATE", "PUT", self.spot_margin_url, endpoint)

    def delete_listen_key(self):
        """
        PRIVATE DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        Creates a websocket listen key for authenticated connections
        valid for 60 mins
        doing a put request will extend by 60 mins
        """
        endpoint = "/api/v3/userDataStream"
        return self.rest_requests("PRIVATE", "DELETE", self.spot_margin_url, endpoint)
