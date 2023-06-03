"""
Spot APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""
import requests

from binance_client import Binance
from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET


class BinanceMargin(Binance):
    """
    Spot APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.spot_margin_url = "https://api.binance.com"
        self.timeout = 5

    ############################
    ### Margin Account/Trade ###
    ############################

    # for isolated margin accounts

    def get_isolated_margin_info(self) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/isolated/account"
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_margin_loan_records(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-loan-record-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	NO
            symbol 	    STRING 	YES
            transFrom 	STRING 	NO 	"SPOT", "ISOLATED_MARGIN"
            transTo 	STRING 	NO 	"SPOT", "ISOLATED_MARGIN"
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            current 	LONG 	NO 	Current page, default 1
            size 	    LONG 	NO 	Default 10, max 100
            archived 	STRING 	NO 	Default: false. Set to true
                                    for archived data from 6 months ago
            recvWindow 	LONG 	NO 	No more than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/loan", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_isolated_margin_transfer_history(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-isolated-margin-transfer-history-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	NO
            symbol 	    STRING 	YES
            transFrom 	STRING 	NO 	"SPOT", "ISOLATED_MARGIN"
            transTo 	STRING 	NO 	"SPOT", "ISOLATED_MARGIN"
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            current 	LONG 	NO 	Current page, default 1
            size 	    LONG 	NO 	Default 10, max 100
            archived 	STRING 	NO 	Default: false. Set to true
                                    for archived data from 6 months ago
            recvWindow 	LONG 	NO 	No more than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/isolated/transfer", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_interest_history(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            asset 	        STRING 	NO
            isolatedSymbol 	STRING 	NO 	isolated symbol
            startTime 	    LONG 	NO
            endTime 	    LONG 	NO
            current 	    LONG 	NO 	Currently querying page. Start from 1. Default:1
            size 	        LONG 	NO 	Default:10 Max:100
            archived 	    STRING 	NO 	Default: false
            recvWindow 	    LONG 	NO 	The value cannot be greater than 60000
            timestamp 	    LONG 	YES

        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/interestHistory", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_orderbook(self, params: dict) -> dict:
        # public request
        # https://binance-docs.github.io/apidocs/spot/en/#order-book
        # same order book as for spot
        """
        Args:
            params (dict):
            Name    Type    Mandatory   Description
            symbol 	STRING 	YES
            limit 	INT 	NO 	Default 100; max 5000.
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/depth", params, timeout=self.timeout
        )
        data = response.json()
        return data

    def margin_new_order(self, params: dict) -> dict:
        """
        private POST request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

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
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/order", params
        )
        response = requests.post(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def margin_cancel_order(self, params: dict) -> dict:
        """
        private DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            isIsolated 	        STRING 	NO 	TRUE or FALSE
            orderId 	        LONG 	NO
            origClientOrderId 	STRING 	NO
            newClientOrderId 	STRING 	NO
            recvWindow 	        LONG 	NO 	The value cannot be greater than 60000
            timestamp 	        LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/order", params
        )
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def margin_open_orders(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-orders-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	NO
            isIsolated 	STRING 	NO 	for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
            recvWindow 	LONG 	NO 	The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/openOrders", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_margin_trade_list(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            isIsolated 	STRING 	NO 	for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
            orderId 	LONG 	NO
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            fromId 	    LONG 	NO 	TradeId to fetch from. Default gets most recent trades.
            limit 	    INT 	NO 	Default 500; max 1000.
            recvWindow 	LONG 	NO 	The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/margin/myTrades", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data


if __name__ == "__main__":
    client = BinanceMargin(BINANCE_KEY, BINANCE_SECRET)
    margin_acc_info = client.get_isolated_margin_info()
