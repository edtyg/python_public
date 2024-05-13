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

from local_credentials.api_work.crypto_exchanges.bybit import (
    BYBIT_MCA_MAIN_READ,
    BYBIT_MCA_MAIN_TRADE,
)


class Bybit:
    """Rest API for bybit"""

    def __init__(self, apikey: str, apisecret: str):
        self.api_key = apikey
        self.api_secret = apisecret

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

    def get_server_time(self, params: Optional[Dict] = None):
        """
        Gets Bybit Server Time
        https://bybit-exchange.github.io/docs/v5/market/time
        """
        endpoint = "/v5/market/time"
        return self._get(endpoint, params)

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


if __name__ == "__main__":
    account = BYBIT_MCA_MAIN_TRADE
    client = Bybit(
        account["api_key"],
        account["api_secret"],
    )

    int_transf = client.get_internal_transfer_records()
    print(int_transf)
