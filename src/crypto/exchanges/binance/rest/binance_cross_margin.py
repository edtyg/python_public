"""
Spot Margin APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

import requests

from src.crypto.exchanges.binance.rest.binance_client import Binance


class BinanceCrossMargin(Binance):
    """
    Spot Margin subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.binance_margin_base_url = "https://api.binance.com"
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

    ###############
    ### Methods ###
    ###############

    def post_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-repay-margin

        Margin account borrow/repay(MARGIN) Cross + Isolated

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	YES         "BTC"
            isisolated  STRING  YES         True for isolated, False for cross
            symbol      STRING  YES         only for isolated margin
            amount      STRING  YES
            type        STRING  YES         BORROW or REPAY
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        endpoint = "/sapi/v1/margin/borrow-repay"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._post(url)

    def get_margin_account_borrow_repay(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-borrow-repay-records-in-margin-account-user_data

        Query borrow/repay records in Margin account Cross + Isolated

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
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        endpoint = "/sapi/v1/margin/borrow-repay"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._post(url)

    ######################
    ### Placing Orders ###
    ######################

    def post_margin_new_order(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

        Post a new order for margin account - Cross + Isolated

        Args:
            params (dict):
            Name                    Type        Mandatory   Description
            symbol 	                STRING 	    YES
            isIsolated 	            STRING 	    NO 	        True or False
            side 	                ENUM 	    YES 	    BUY or SELL
            type 	                ENUM 	    YES
            quantity 	            DECIMAL 	NO
            quoteOrderQty 	        DECIMAL 	NO
            price 	                DECIMAL 	NO
            stopPrice 	            DECIMAL 	NO
            newClientOrderId 	    STRING 	    NO 	Automatically generated if not sent.
            icebergQty 	            DECIMAL 	NO
            newOrderRespType 	    ENUM 	    NO
            sideEffectType 	        ENUM 	    NO  NO_SIDE_EFFECT - manual borrow and repay
                                                    MARGIN_BUY - auto borrow if nt enough assets
                                                    AUTO_REPAY - auto repay liabilities on rcvd assets
                                                    AUTO_BORROW_REPAY - combine MARGIN_BUY and AUTO_REPAY
            timeInForce 	        ENUM 	    NO 	GTC,IOC,FOK
            selfTradePreventionMode ENUM        NO
            autoRepayAtCancel       BOOL        NO
            recvWindow 	            LONG 	    NO 	The value cannot be greater than 60000
            timestamp 	            LONG 	    YES
        """
        endpoint = "/sapi/v1/margin/order"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._post(url)

    def delete_margin_cancel_order(self, params: dict) -> dict:
        """
        PRIVATE
        DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

        Cancel an active order for margin account - Cross + Isolated

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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._delete(url)

    def delete_margin_cancel_all_open_orders(self, params: dict) -> dict:
        """
        PRIVATE
        DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-all-open-orders-on-a-symbol-trade

        Cancels all active orders on a symbol for margin account - Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated 	        STRING 	NO 	        TRUE or FALSE
            recvWindow 	        LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	        LONG 	YES
        """
        endpoint = "/sapi/v1/margin/openOrders"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._delete(url)

    def get_interest_history(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data

        Gets interest history - Cross + Isolated

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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)

    def get_cross_margin_details(self) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-account-details-user_data

        Use this for cross margin account details and balances
        """
        endpoint = "/sapi/v1/margin/account"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint)
        return self._get(url)

    def get_margin_account_order(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)

    def get_margin_account_open_orders(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-orders-user_data
        Gets all open orders - Cross + Isolated

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated          STRING  NO          TRUE or FALSE
        """
        endpoint = "/sapi/v1/margin/openOrders"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)

    def get_margin_account_all_orders(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-orders-user_data

        Gets historical orders - Cross + Isolated

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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)

    def get_margin_account_trades(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data

        Gets historical margin trades - Cross + Isolated

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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)

    def get_isolated_margin_details(self) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data

        Use this for isolated margin account details and balances
        """
        endpoint = "/sapi/v1/margin/isolated/account"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint)
        return self._get(url)

    #######################
    ### toggle bnb burn ###
    #######################

    def post_toggle_bnb_burn(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._post(url)

    def get_bnb_burn_status(self) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
        """
        endpoint = "/sapi/v1/bnbBurn"
        url = self.signed_request_url(self.binance_margin_base_url, endpoint)
        return self._get(url)

    ######################
    ### post transfers ###
    ######################

    def post_universal_transfer(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._post(url)

    ########################
    ### Get Capital Flow ###
    ########################

    def get_capital_flow(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
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
        url = self.signed_request_url(self.binance_margin_base_url, endpoint, params)
        return self._get(url)
