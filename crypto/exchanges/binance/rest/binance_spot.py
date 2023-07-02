"""
Spot APIs
https://binance-docs.github.io/apidocs/spot/en/#change-log
"""
from typing import Dict, Optional

import requests
from python.crypto.exchanges.binance.rest.binance_client import Binance
from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET


class BinanceSpot(Binance):
    """
    Spot APIs subclass for binance
    """

    def __init__(self, apikey: str, apisecret: str):
        super().__init__(apikey, apisecret)
        self.spot_margin_url = "https://api.binance.com"
        self.timeout = 5

    ########################
    ### wallet endpoints ###
    ########################

    def get_system_status(self) -> dict:
        """
        public GET request
        https://binance-docs.github.io/apidocs/spot/en/#system-status-system
        """
        response = requests.get(
            self.spot_margin_url + "/sapi/v1/system/status", timeout=self.timeout
        )
        data = response.json()
        return data

    def get_all_coins_infomation(self) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/capital/config/getall"
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_daily_account_snapshot(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            type 	    STRING 	YES 	    "SPOT", "MARGIN", "FUTURES"
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	        min 7, max 30, default 7
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/accountSnapshot", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_deposit_history(self, params: Optional[Dict] = None) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            coin 	    STRING 	NO
            status 	    INT 	NO 	0(0:pending,6: credited but cannot withdraw, 1:success)
            startTime 	LONG 	NO 	Default: 90 days from current timestamp
            endTime 	LONG 	NO 	Default: present timestamp
            offset 	    INT 	NO 	Default:0
            limit 	    INT 	NO 	Default:1000, Max:1000
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
            txId 	    STRING 	NO
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/capital/deposit/hisrec", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_withdrawal_history(self, params: Optional[Dict] = None) -> dict:
        """
        private GET request
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
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/capital/withdraw/history", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_deposit_address(self, params: dict) -> dict:
        """
        private GET request
        https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            coin 	    STRING 	YES
            network 	STRING 	NO
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/capital/deposit/address", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_asset_detail(self, params: Optional[Dict] = None) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#asset-detail-user_data
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            asset 	    STRING 	NO
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/asset/assetDetail", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_trade_fee(self, params: Optional[Dict] = None) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#trade-fee-user_data
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	NO
            recvWindow 	LONG 	NO
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v1/asset/tradeFee", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_user_asset(self, params: Optional[Dict] = None) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#user-asset-user_data
        """
        Args:
            params (dict):
            Name                Type    Mandatory   Description
            asset 	            STRING 	NO
            needBtcValuation 	LONG 	NO
            recvWindow 	        LONG 	NO
            timestamp 	        LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/sapi/v3/asset/getUserAsset", params
        )
        response = requests.post(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    #############################
    ### market data endpoints ###
    #############################

    def get_test_connectivity(self) -> dict:
        """
        public request
        https://binance-docs.github.io/apidocs/spot/en/#test-connectivity
        Test connectivity to the Rest API.
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/ping", timeout=self.timeout
        )
        data = response.json()
        return data

    def get_check_server_time(self) -> dict:
        """
        public request
        https://binance-docs.github.io/apidocs/spot/en/#check-server-time
        Test connectivity to the Rest API and get the current server time
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/time", timeout=self.timeout
        )
        data = response.json()
        return data

    def get_exchange_infomation(self) -> dict:
        """
        public request
        https://binance-docs.github.io/apidocs/spot/en/#exchange-information
        Current exchange trading rules and symbol information
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/exchangeInfo", timeout=self.timeout
        )
        data = response.json()
        return data

    def get_orderbook(self, params: dict) -> dict:
        # public request
        # https://binance-docs.github.io/apidocs/spot/en/#order-book
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

    def get_recent_trade_list(self, params: dict) -> dict:
        # public request
        # https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list
        """
        Args:
            params (dict):
            Name    Type    Mandatory   Description
            symbol 	STRING 	YES
            limit 	INT 	NO 	Default 100; max 5000.
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/trades", params, timeout=self.timeout
        )
        data = response.json()
        return data

    def get_kline(self, params: dict) -> dict:
        # public request
        # https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	YES
            interval 	ENUM 	YES
            startTime 	LONG 	NO
            endTime 	LONG 	NO
            limit 	    INT 	NO 	Default 500; max 1000.
        """
        response = requests.get(
            self.spot_margin_url + "/api/v3/klines", params, timeout=self.timeout
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

    ############################
    ### spot account / trade ###
    ############################

    def post_new_order(self, params: dict) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
        # Send in a new order.
        """
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
        url = self.signed_request_url(self.spot_margin_url, "/api/v3/order", params)
        response = requests.post(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def delete_cancel_order(self, params: dict) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade
        # Cancel an active order.
        """
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
        url = self.signed_request_url(self.spot_margin_url, "/api/v3/order", params)
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_query_order(self, params: dict) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data
        # Check an order's status.
        """
        Args:
            params (dict):
            Name                Type    Mandatory   Description
            symbol 	            STRING 	YES
            orderId 	        LONG 	NO
            origClientOrderId 	STRING 	NO
            recvWindow 	        LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	        LONG 	YES
        """
        url = self.signed_request_url(self.spot_margin_url, "/api/v3/order", params)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_current_open_orders(self, params: Optional[Dict] = None) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
        # Check an order's status.
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            symbol 	    STRING 	NO
            recvWindow 	LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(
            self.spot_margin_url, "/api/v3/openOrders", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_all_orders(self, params: dict) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data
        # Get all account orders; active, canceled, or filled.
        """
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
        url = self.signed_request_url(
            self.spot_margin_url, "/api/v3/openOrders", params
        )
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data

    def get_account_infomation(self) -> dict:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data
        # Get current account information.
        """
        Args:
            params (dict):
            Name        Type    Mandatory   Description
            recvWindow 	LONG 	NO 	        The value cannot be greater than 60000
            timestamp 	LONG 	YES
        """
        url = self.signed_request_url(self.spot_margin_url, "/api/v3/account")
        response = requests.get(
            url, headers=self.headers, timeout=self.timeout
        )  # signed request
        data = response.json()
        return data

    def get_account_trade_list(self, params: dict) -> list:
        # private request
        # https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data
        # Get trades for a specific account and symbol.
        """
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
        url = self.signed_request_url(self.spot_margin_url, "/api/v3/myTrades", params)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = response.json()
        return data


if __name__ == "__main__":
    client = BinanceSpot(BINANCE_KEY, BINANCE_SECRET)

    trade_list = client.get_account_trade_list(params={"symbol": "BTCBUSD"})
    print(trade_list)

    t = client.get_symbol_price_ticker({"symbol": "BTCUSDT"})
    assets = client.get_user_asset()
