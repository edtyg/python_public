"""
BYBIT v5 APIs
https://bybit-exchange.github.io/docs/v5/intro
"""

import datetime as dt
import hashlib
import hmac
import json
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


class Bybit:
    """Rest API for bybit"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

        self.bybit_base_url = "https://api.bybit.com"
        self.recv_window = str(5000)
        self.headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": None,
            "X-BAPI-TIMESTAMP": None,
            "X-BAPI-RECV-WINDOW": self.recv_window,
            "Content-Type": "application/json",
        }
        self.timeout = 3

    def get_current_timestamp(self):
        """gets current timestamp in milliseconds"""
        timestamp = str(int(dt.datetime.now().timestamp()) * 1000)
        return timestamp

    def generate_signature(self, method: str, payload: dict):
        """generates signature"""
        timestamp = self.get_current_timestamp()

        if payload is None:
            query_string = ""
        elif method == "GET" and payload:
            query_string = urlencode(payload, True)
        elif method == "POST" and payload:
            query_string = json.dumps(payload)

        param_str = timestamp + self.api_key + self.recv_window + query_string
        hashing = hmac.new(
            bytes(self.api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256
        )
        signature = hashing.hexdigest()
        self.headers["X-BAPI-SIGN"] = signature
        self.headers["X-BAPI-TIMESTAMP"] = timestamp

    #############################
    ### Standardized requests ###
    #############################

    def _get(self, endpoint: str, params: Optional[Dict] = None):
        """GET Request"""
        self.generate_signature("GET", params)
        response = requests.get(
            url=self.bybit_base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def _post(self, endpoint: str, params: Optional[Dict] = None):
        """POST Request"""
        self.generate_signature("POST", params)
        response = requests.post(
            url=self.bybit_base_url + endpoint,
            headers=self.headers,
            json=params,
            timeout=self.timeout,
        )
        return response.json()

    ##############
    ### Market ###
    ##############
    def get_kline(self, params: dict):
        """
        Gets Klines
        https://bybit-exchange.github.io/docs/v5/market/kline

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            category    false   string      spot, linear, inverse
            symbol      true    string      symbol name
            interval    true    string      1,3,5,15,30,60,D,M,W
            start       false   int         start timestamp milliseconds
            end         false   integer     end timestamp milliseconds
            limit       false   integer     [1,2000] default 200
        """
        endpoint = "/v5/market/kline"
        return self._get(endpoint, params)

    def get_instruments_info(self, params: dict):
        """
        Gets instruments
        https://bybit-exchange.github.io/docs/v5/market/instrument

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            category    true    str         spot, linear, inverse, option
            symbol      false   str         symbol name
            status      false   str
            baseCoin    false   str         start timestamp milliseconds
            limit       false   integer     [1,2000] default 200
        """
        endpoint = "/v5/market/instruments-info"
        return self._get(endpoint, params)

    def get_orderbook(self, params: dict):
        """
        Query for orderbook depth data.
        Covers: Spot / USDT perpetual / USDC contract / Inverse contract / Option
        https://bybit-exchange.github.io/docs/v5/market/orderbook

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            category    true    str         spot, linear, inverse, option
            symbol      false   str         symbol name
            status      false   str
            baseCoin    false   str         start timestamp milliseconds
            limit       false   integer     [1,2000] default 200
        """
        endpoint = "/v5/market/orderbook"
        return self._get(endpoint, params)

    def get_tickers(self, params: dict):
        """
        Query for the latest price snapshot,
        best bid/ask price, and trading volume in the last 24 hours.
        Covers: Spot / USDT perpetual / USDC contract / Inverse contract / Option

        https://bybit-exchange.github.io/docs/v5/market/tickers

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            category    true    str         spot, linear, inverse, option
            symbol      false   str         symbol name
            baseCoin    false   str         start timestamp milliseconds
        """
        endpoint = "/v5/market/tickers"
        return self._get(endpoint, params)

    def get_funding_rate_history(self, params: dict):
        """
        Query for historical funding rates. Each symbol has a different funding interval.
        For example, if the interval is 8 hours and the current time is UTC 12,
        then it returns the last funding rate, which settled at UTC 8.

        https://bybit-exchange.github.io/docs/v5/market/history-fund-rate

        Args:
            params (dict):
            Name        Type    Mandatory   Description
            category    true    str         spot, linear, inverse, option
            symbol      false   str         symbol name
            startTime   false   int         start time in timestamp ms
            endTime     false   int         end time in timestamp ms
        """
        endpoint = "/v5/market/funding/history"
        return self._get(endpoint, params)

    #############
    ### Trade ###
    #############

    def place_order(self, params: dict):
        """
        This endpoint supports to create the order for spot, spot margin,
        USDT perpetual, USDC perpetual, USDC futures, inverse futures and options.

        https://bybit-exchange.github.io/docs/v5/order/create-order

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            isLeverage  false       int         default 0 = false, 1 = true
            side        true        str         "Buy" or "Sell"
            orderType   true        str         "Market" or "Limit"
            qty         true        str         UTA: default quoteCoin for market buy and baseCoin for market sell
            marketUnit  false       str         baseCoin or quoteCoin
            price       false       str
            timeInForce false       str         default IOC for market order, GTC for limit order
            orderLinkId false       str         customized order id max 36 characters - unique cannot reuse
        """
        endpoint = "/v5/order/create"
        return self._post(endpoint, params)

    def amend_order(self, params: dict):
        """
        Unified account covers: Spot / USDT perpetual / USDC contract / Inverse contract / Option
        Classic account covers: Spot / USDT perpetual / Inverse contract

        https://bybit-exchange.github.io/docs/v5/order/amend-order

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            orderId     false       string      Order ID. Either orderId or orderLinkId is required
            orderLinkId false       string      User customised order ID. Either orderId or orderLinkId is required
            qty         true        str         Order quantity after modification. Do not pass it if not modify the qty
            price       false       str         Order price after modification. Do not pass it if not modify the price
        """
        endpoint = "/v5/order/amend"
        return self._post(endpoint, params)

    def cancel_order(self, params: dict):
        """
        Unified account covers: Spot / USDT perpetual / USDC contract / Inverse contract / Option
        Classic account covers: Spot / USDT perpetual / Inverse contract

        https://bybit-exchange.github.io/docs/v5/order/cancel-order

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            orderId     false       string      Order ID. Either orderId or orderLinkId is required
            orderLinkId false       string      User customised order ID. Either orderId or orderLinkId is required
        """
        endpoint = "/v5/order/cancel"
        return self._post(endpoint, params)

    def get_open_orders(self, params: dict):
        """
        Query unfilled or partially filled orders in real-time.
        To query older order records, please use the order history interface.

        https://bybit-exchange.github.io/docs/v5/order/open-order

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            baseCoin    false       string      supports linear, inverse & option
            settleCoin  fasle       string      linear: either symbol, baseCoin or settleCoin is required
            orderId     false       string      Order ID. Either orderId or orderLinkId is required
            orderLinkId false       string      User customised order ID. Either orderId or orderLinkId is required
            limit       false       int         default = 20, [1,50]
        """
        endpoint = "/v5/order/realtime"
        return self._get(endpoint, params)

    def cancel_all_orders(self, params: dict):
        """
        Query unfilled or partially filled orders in real-time.
        To query older order records, please use the order history interface.

        https://bybit-exchange.github.io/docs/v5/order/cancel-all

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            baseCoin    false       string      supports linear, inverse & option
            settleCoin  fasle       string      linear: either symbol, baseCoin or settleCoin is required
        """
        endpoint = "/v5/order/cancel-all"
        return self._post(endpoint, params)

    def get_order_history(self, params: dict):
        """
        up to 2 years
        Query order history. As order creation/cancellation is asynchronous,
        the data returned from this endpoint may delay.
        If you want to get real-time order information,
        you could query this endpoint or rely on the websocket stream (recommended).

        https://bybit-exchange.github.io/docs/v5/order/order-list

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            baseCoin    false       string      supports linear, inverse & option
            settleCoin  fasle       string      linear: either symbol, baseCoin or settleCoin is required
            orderId     false       string      Order ID. Either orderId or orderLinkId is required
            orderLinkId false       string      User customised order ID. Either orderId or orderLinkId is required
            startTime   false       int         milliseconds
            endTime     false       int         milliseconds
            limit       false       int         default = 20, [1,50]
            cursor      false       str         Use the nextPageCursor token from the response to retrieve the next page of the result set
        """
        endpoint = "/v5/order/history"
        return self._get(endpoint, params)

    def get_trade_history(self, params: dict):
        """
        up to 2 years
        Query order history. As order creation/cancellation is asynchronous,
        the data returned from this endpoint may delay.
        If you want to get real-time order information,
        you could query this endpoint or rely on the websocket stream (recommended).

        https://bybit-exchange.github.io/docs/v5/order/execution

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            orderId     false       string      Order ID. Either orderId or orderLinkId is required
            orderLinkId false       string      User customised order ID. Either orderId or orderLinkId is required
            baseCoin    false       string      supports linear, inverse & option
            startTime   false       int         milliseconds
            endTime     false       int         milliseconds
            limit       false       int         default = 20, [1,50]
            cursor      false       str         Use the nextPageCursor token from the response to retrieve the next page of the result set
        """
        endpoint = "/v5/execution/list"
        return self._get(endpoint, params)

    ################
    ### position ###
    ################

    def get_position_info(self, params: dict):
        """
        Query real-time position data, such as position size, cumulative realizedPNL.
        https://bybit-exchange.github.io/docs/v5/position

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      for unified acc: "spot", "linear", "inverse", "option
            symbol      true        string      Symbol
            baseCoin    false       string      supports linear, inverse & option
            settleCOin  false       string      supports linear, inverse & option
            limit       false       int         default = 20, [1,50]
            cursor      false       str         Use the nextPageCursor token from the response to retrieve the next page of the result se
        """
        endpoint = "/v5/position/list"
        return self._get(endpoint, params)

    ###############
    ### Account ###
    ###############

    def get_wallet_balance(self, params: dict):
        """gets wallet balance
        Use this for trading accounts (non funding)
        https://bybit-exchange.github.io/docs/v5/account/wallet-balance

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            accountType true        string      UNIFIED, CONTRACT, SPOT
        """
        endpoint = "/v5/account/wallet-balance"
        return self._get(endpoint, params)

    def post_repay_liability(self, params: dict):
        """
        You can manually repay the liabilities of Unified account
        https://bybit-exchange.github.io/docs/v5/account/repay-liability

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            coin        false       string      UNIFIED, CONTRACT, SPOT
        """
        endpoint = "/v5/account/quick-repayment"
        return self._post(endpoint, params)

    def post_set_collateral_coin(self, params: dict):
        """
        You can decide whether the assets in the Unified account needs to be collateral coins.
        https://bybit-exchange.github.io/docs/v5/account/set-collateral

        Args:
            params (dict):
            Parameter           Required    Type        Comments
            coin                true        string      BTC, ETH...
            collateralSwitch    true        string      "ON" or "OFF"
        """
        endpoint = "/v5/account/set-collateral-switch"
        return self._post(endpoint, params)

    def get_collateral_info(self, params: dict = None):
        """Get the collateral information of the current unified margin account,
        including loan interest rate, loanable amount,
        collateral conversion rate,
        whether it can be mortgaged as margin, etc.

        https://bybit-exchange.github.io/docs/v5/account/collateral-info

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            currency    false       string
        """
        endpoint = "/v5/account/collateral-info"
        return self._get(endpoint, params)

    def get_fee_rate(self, params: dict):
        """Get the trading fee rate.

        Use this for trading accounts (non funding)
        https://bybit-exchange.github.io/docs/v5/account/fee-rate

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            category    true        string      spot, linear, inverse, option
            symbol      false       string      Symbol name. Valid for linear, inverse, spot
            baseCoin    false       string      Base coin. SOL, BTC, ETH. Valid for option
        """
        endpoint = "/v5/account/fee-rate"
        return self._get(endpoint, params)

    def get_account_info(self, params: dict = None):
        """Query the margin mode configuration of the account.

        https://bybit-exchange.github.io/docs/v5/account/account-info
        """
        endpoint = "/v5/account/info"
        return self._get(endpoint, params)

    def post_set_margin_mode(self, params: dict = None):
        """Default is regular margin mode

        https://bybit-exchange.github.io/docs/v5/account/set-margin-mode
        """
        endpoint = "/v5/account/set-margin-mode"
        return self._post(endpoint, params)

    #############
    ### Asset ###
    #############

    def get_all_coins_balance(self, params: dict):
        """
        You could get all coin balance of all account types
        under the master account, and sub account.

        Use this for funding account
        https://bybit-exchange.github.io/docs/v5/asset/all-balance


        Args:
            params (dict):
            Parameter   Required    Type        Comments
            memberId    false       string      User Id
            accountType true        string      e.g. FUND, UNIFIED, CONTRACT
            coin        false       string
            withBonus   false       integer
        """
        endpoint = "/v5/asset/transfer/query-account-coins-balance"
        return self._get(endpoint, params)

    def get_internal_transfer_records(self, params: Optional[Dict] = None):
        """
        Query the internal transfer records between different account types under the same UID.
        https://bybit-exchange.github.io/docs/v5/asset/inter-transfer-list

        Args:
            params (dict):
            Parameter       Required    Type        Comments
            transferId      false       str         UUID. Use the one you generated in createTransfer
            coin            false       str         Coin
            status          false       str         Transfer status
            startTime
            endTime
            limit           false       int         default 20, range[1,50]
        """
        endpoint = "/v5/asset/transfer/query-inter-transfer-list"
        return self._get(endpoint, params)

    def get_universal_transfer_records(self, params: Optional[Dict] = None):
        """
        Query universal transfer records
        https://bybit-exchange.github.io/docs/v5/asset/unitransfer-list

        Args:
            params (dict):
            Parameter       Required    Type        Comments
            transferId      false       str         UUID. Use the one you generated in createTransfer
            coin            false       str         Coin
            status          false       str         Transfer status
            startTime
            endTime
            limit           false       int         default 20, range[1,50]
        """
        endpoint = "/v5/asset/transfer/query-universal-transfer-list"
        return self._get(endpoint, params)

    ############
    ### User ###
    ############

    def get_api_key_info(self, params: Optional[Dict] = None):
        """
        Get the information of the api key.
        Use the api key pending to be checked to call the endpoint.
        Both master and sub user's api key are applicable.

        https://bybit-exchange.github.io/docs/v5/user/apikey-info

        """
        endpoint = "/v5/user/query-api"
        return self._get(endpoint, params)

    ###############################
    ### SPOT Margin Trade (UTA) ###
    ###############################

    def get_vip_margin_data(self, params: Optional[Dict] = None):
        """
        This margin data is for Unified account in particular.
        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/vip-margin

        Args:
            params (dict):
            Parameter       Required    Type        Comments
            vipLevel        false       string      Vip level
            currency        false       string      Coin name, uppercase only
        """
        endpoint = "/v5/spot-margin-trade/data"
        return self._get(endpoint, params)

    def get_status_leverage(self):
        """
        Query the Spot margin status and leverage of Unified account
        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status

        """
        endpoint = "/v5/spot-margin-trade/state"
        return self._get(endpoint)
