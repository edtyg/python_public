"""
Spot APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""

from typing import Dict, Optional

import requests

from src.crypto.exchanges.binance.rest.binance_client import Binance


class BinanceSpot(Binance):
    """
    Spot APIs child class
    Private and public endpoints
    sign using parent class method if private
    no signature required for public endpoints
    """

    def __init__(self, apikey: str = None, apisecret: str = None):
        super().__init__(apikey, apisecret)
        self.binance_spot_base_url = "https://api.binance.com"
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

    ########################
    ### wallet endpoints ###
    ########################

    def get_system_status(self) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#system-status-system
        """
        endpoint = "/sapi/v1/system/status"
        return self._get(self.binance_spot_base_url + endpoint)

    def get_all_coins_infomation(self) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
        """
        endpoint = "/sapi/v1/capital/config/getall"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint)
        return self._get(url)

    def get_deposit_history(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data

        Args:
            params (dict):
            Name            Type    Mandatory   Description
            includeSource   BOOL    NO          default False, incld src address if True
            coin 	        STRING 	NO          "BTC" "ETH" ...
            status 	        INT 	NO 	        0:pending,
                                                6:credited but cannot withdraw
                                                7:Wrong Deposit
                                                8:Waiting User confirm
                                                1:success
            startTime 	    LONG 	NO 	        Default: 90 days from current timestamp
            endTime 	    LONG 	NO 	        Default: present timestamp
            offset 	        INT 	NO 	        Default:0
            limit 	        INT 	NO 	        Default:1000, Max:1000
            recvWindow 	    LONG 	NO
            timestamp 	    LONG 	YES
            txId 	        STRING 	NO
        """
        endpoint = "/sapi/v1/capital/deposit/hisrec"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def get_withdrawal_history(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            coin 	            STRING 	NO
            withdrawOrderId 	STRING 	NO
            status 	            INT 	NO 	        0:Email Sent
                                                    1:Cancelled
                                                    2:Awaiting Approval
                                                    3:Rejected
                                                    4:Processing
                                                    5:Failure
                                                    6:Completed
            offset 	            INT 	NO
            limit 	            INT 	NO 	        Default: 1000, Max: 1000
            startTime 	        LONG 	NO 	        Default: 90 days from current timestamp
            endTime 	        LONG 	NO 	        Default: present timestamp
            recvWindow 	        LONG 	NO
            timestamp 	        LONG 	YES
        """
        endpoint = "/sapi/v1/capital/withdraw/history"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def get_deposit_address(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            coin 	    STRING 	YES
            network 	STRING 	NO
            amount      DECIMAL NO          LIGHTNING NETWORK
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        endpoint = "/sapi/v1/capital/deposit/address"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def get_trade_fee(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#trade-fee-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	NO
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        endpoint = "/sapi/v1/asset/tradeFee"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def post_user_universal_transfer(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer-user_data

        Transfers between spot/margin/futures accounts

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            type	    ENUM	YES
            asset	    STRING	YES
            amount	    DECIMAL	YES
            fromSymbol	STRING	NO
            toSymbol	STRING	NO
            recvWindow	LONG	NO
            timestamp	LONG	YES

        type:
        MAIN_MARGIN -> Main to Cross Margin account
        MAIN_ISOLATED_MARGIN -> Main to Isolated Margin account
        MAIN_UMFUTURE -> Main to usd margined futures account
        MAIN_CMFUTURE -> Main to coin margined futures account
        MAIN_FUNDING -> Main to funding account
        MAIN_OPTION -> Main to Options account
        ...
        Different permutations FROM_TO below
        MAIN / MARGIN / ISOLATED_MARGIN / UMFUTURE / CMFUTURE / FUNDING / OPTION
        /PORTFOLIO_MARGIN
        """
        endpoint = "/sapi/v1/asset/transfer"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._post(url)

    def get_user_universal_transfer(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-user-universal-transfer-history-user_data

        Get transfer records between accounts

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            type	    ENUM	YES
            startTime	LONG	NO
            endTime	    LONG	NO
            current	    INT	    NO	        Default 1
            size	    INT	    NO	        Default 10, Max 100
            fromSymbol	STRING	NO
            toSymbol	STRING	NO
            recvWindow	LONG	NO
            timestamp	LONG	YES
        """
        endpoint = "/sapi/v1/asset/transfer"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def post_user_asset(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/spot/en/#user-asset-user_data
        Args:
            params (dict):
            Name                Type    Mandatory   Description
            asset 	            STRING 	NO
            needBtcValuation 	LONG 	NO
            recvWindow 	        LONG 	NO
            timestamp 	        LONG 	YES
        """
        endpoint = "/sapi/v3/asset/getUserAsset"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._post(url)

    def get_user_wallet_balance(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-user-wallet-balance-user_data

        gets balances from each wallet - in btc terms

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            recvWindow 	        LONG 	NO
            timestamp 	        LONG 	YES
        """
        endpoint = "/sapi/v1/asset/wallet/balance"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    #############################
    ### sub-account endpoints ###
    #############################

    def get_subacc_transfer_history(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#sub-account-transfer-history-for-sub-account
        Sub-account Transfer History (For Sub-account) - query using sub acc api key

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            asset	            STRING	NO	        If not sent, result of all assets will be returned
            type	            INT	NO	            1: transfer in, 2: transfer out
            startTime	        LONG	NO
            endTime	            LONG	NO
            limit	            INT	    NO	        Default 500
            returnFailHistory	BOOLEAN	NO	        Default False,
                                                    return PROCESS and SUCCESS status history;
                                                    If True,return PROCESS and SUCCESS and FAILURE status history
            recvWindow	        LONG	NO
            timestamp	        LONG	YES
        """
        endpoint = "/sapi/v1/sub-account/transfer/subUserHistory"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    #############################
    ### market data endpoints ###
    #############################

    def get_orderbook(self, params: dict) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#order-book

        Args:
            params (dict):
            Name    Type    Mandatory   Description
            symbol 	STRING 	YES
            limit 	INT 	NO 	        Default 100; max 5000.
        """
        endpoint = "/api/v3/depth"
        response = requests.get(
            self.binance_spot_base_url + endpoint,
            params,
            timeout=self.timeout,
        )
        return response.json()

    def get_kline(self, params: dict) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            interval 	ENUM 	YES
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	        Default 500; max 1000.
        """
        endpoint = "/api/v3/klines"
        response = requests.get(
            self.binance_spot_base_url + endpoint,
            params,
            timeout=self.timeout,
        )
        return response.json()

    def get_symbol_price_ticker(self, params: dict) -> dict:
        """
        PUBLIC
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES         "BTCUSDT"
            symbols     STRING 	YES         ["BTCUSDT","BNBUSDT"] either symbol or symbols
        """
        endpoint = "/api/v3/ticker/price"
        response = requests.get(
            self.binance_spot_base_url + endpoint,
            params,
            timeout=self.timeout,
        )
        return response.json()

    ############################
    ### spot account / trade ###
    ############################

    def post_order(self, params: dict) -> dict:
        """
        PRIVATE
        POST request
        https://binance-docs.github.io/apidocs/spot/en/#new-order-trade

        Send in a new order.

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            symbol 	            STRING 	    YES
            side 	            ENUM 	    YES
            type 	            ENUM 	    YES
            timeInForce 	    ENUM 	    NO          GTC, IOC, FOK
            quantity 	        DECIMAL 	NO
            quoteOrderQty 	    DECIMAL 	NO
            price 	            DECIMAL 	NO
            newClientOrderId 	STRING 	    NO
            strategyId 	        INT 	    NO
            strategyType 	    INT 	    NO
            stopPrice 	        DECIMAL 	NO
            trailingDelta 	    LONG 	    NO
            icebergQty 	        DECIMAL 	NO
            newOrderResp        Type 	    ENUM
            recvWindow  	    LONG 	    NO
            timestamp 	        LONG 	    YES

            order types and additional mandatory params:
            Type 	            Additional mandatory parameters
            LIMIT 	            timeInForce, quantity, price
            MARKET 	            quantity or quoteOrderQty
            STOP_LOSS 	        quantity, stopPrice or trailingDelta
            STOP_LOSS_LIMIT 	timeInForce, quantity, price, stopPrice or trailingDelta
            TAKE_PROFIT 	    quantity, stopPrice or trailingDelta
            TAKE_PROFIT_LIMIT 	timeInForce, quantity, price, stopPrice or trailingDelta
            LIMIT_MAKER 	    quantity, price
        """
        endpoint = "/api/v3/order"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._post(url)

    def delete_order(self, params: dict) -> dict:
        """
        PRIVATE
        DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade

        Cancel an active order.

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            symbol 	            STRING 	    YES
            orderId 	        LONG 	    NO
            origClientOrderId 	STRING  	NO
            newClientOrderId 	STRING 	    NO
            recvWindow 	        LONG 	    NO
            timestamp 	        LONG 	    YES
        """
        endpoint = "/api/v3/order"
        url = self.signed_request_url(
            self.binance_spot_base_url,
            endpoint,
            params,
        )
        return self._delete(url)

    def delete_all_open_orders(self, params: dict) -> dict:
        """
        PRIVATE
        DELETE request
        https://binance-docs.github.io/apidocs/spot/en/#cancel-all-open-orders-on-a-symbol-trade

        Cancels all active orders on a symbol.

        Args:
            params (dict):
            Name                Type        Mandatory   Description
            symbol 	            STRING 	    YES
            recvWindow 	        LONG 	    NO
            timestamp 	        LONG 	    YES
        """
        endpoint = "/api/v3/openOrders"
        url = self.signed_request_url(
            self.binance_spot_base_url,
            endpoint,
            params,
        )
        return self._delete(url)

    def get_query_order(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data

        Check an order's status.

        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            orderId 	        LONG 	NO
            origClientOrderId 	STRING 	NO
            recvWindow 	        LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	        LONG 	YES
        """
        endpoint = "/api/v3/order"
        url = self.signed_request_url(
            self.binance_spot_base_url,
            endpoint,
            params,
        )
        return self._get(url)

    def get_current_open_orders(self, params: Optional[Dict] = None) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data

        Get all open orders on a symbol. Careful when accessing this with no symbol.

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	NO
            recvWindow 	LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        endpoint = "/api/v3/openOrders"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def get_all_orders(self, params: dict) -> dict:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data

        Get all account orders; active, canceled, or filled.

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            orderId 	LONG 	NO
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	        Default 500; max 1000.
            recvWindow 	LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        endpoint = "/api/v3/allOrders"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)

    def get_account_trade_list(self, params: dict) -> list:
        """
        PRIVATE
        GET request
        https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data

        Get trades for a specific account and symbol.

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            orderId 	LONG 	NO 	        This can only be used in combination with symbol.
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            fromId 	    LONG 	NO 	        TradeId to fetch from. Default gets most recent trades.
            limit 	    INT 	NO 	        Default 500; max 1000.
            recvWindow 	LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        endpoint = "/api/v3/myTrades"
        url = self.signed_request_url(self.binance_spot_base_url, endpoint, params)
        return self._get(url)
