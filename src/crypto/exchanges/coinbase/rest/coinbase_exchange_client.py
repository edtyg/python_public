"""
Coinbase Exchange APIs - different from brokerage api
https://docs.cdp.coinbase.com/exchange/docs/welcome/
"""

import base64
import datetime as dt
import hashlib
import hmac
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


class CoinbaseExchange:
    """Rest API Client for Coinbase Exchange"""

    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.coinbase_exchange_base_url = "https://api.exchange.coinbase.com"

        self.headers = {
            "cb-access-key": self.api_key,
            "cb-access-passphrase": self.passphrase,
            "Content-Type": "application/json",
        }
        self.timeout = 3

    def get_current_timestamp(self):
        """gets current timestamp in seconds"""
        timestamp = str(int(dt.datetime.now().timestamp()))
        return timestamp

    def generate_signature(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
    ):
        """generates signature"""
        timestamp = self.get_current_timestamp()

        if params is None:
            query_string = ""
        else:
            query_string = "?" + urlencode(params)

        param_str = timestamp + method + endpoint + query_string
        key = base64.b64decode(self.api_secret)
        h = hmac.new(key, param_str.encode("utf-8"), hashlib.sha256)
        cb_access_sign = base64.b64encode(h.digest()).decode("utf-8")

        self.headers["cb-access-sign"] = cb_access_sign
        self.headers["cb-access-timestamp"] = timestamp

    #############################
    ### Standardized requests ###
    #############################

    def _get(self, endpoint: str, params: Optional[Dict] = None):
        """Get Request"""
        self.generate_signature(method="GET", endpoint=endpoint, params=params)
        response = requests.get(
            url=self.coinbase_exchange_base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    ################
    ### Accounts ###
    ################

    def get_all_accounts(self, params: Optional[Dict] = None):
        """Get a list of trading accounts from the profile of the API key.
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounts

        Args:
            params (dict):
            Parameter   Required    Type        Comments
        """
        endpoint = "/accounts"
        return self._get(endpoint, params)

    def get_single_account_ledger(self, account_id: str):
        """
        Lists ledger activity for an account.
        This includes anything that would affect the accounts balance - transfers, trades, fees, etc.
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccountledger

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            account_id  yes         str         account id
                                                USD: 32ba4ec5-a43a-4bbf-b526-ebdcda1d8b83
                                                USDT: ed28240e-07a9-4acc-af62-722f671e5733
                                                USDC: d04b51ca-4e71-40f6-8363-6a59afba968e
        """
        endpoint = f"/accounts/{account_id}/ledger"
        return self._get(endpoint)

    ###################
    ### conversions ###
    ###################

    def get_conversion_fees(self):
        """
        Gets a list of current conversion fee rates and trailing 30 day volume by currency pair
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getconversionfees
        """
        endpoint = "/conversions/fees"
        return self._get(endpoint)

    def get_conversion(self, conversion_id: str):
        """
        Gets a currency conversion by id (i.e. USD -> USDC).
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getconversion
        """
        endpoint = f"/conversions/{conversion_id}"
        return self._get(endpoint)

    #################
    ### Transfers ###
    #################

    def get_all_transfers(self, params: Optional[Dict] = None):
        """
        Gets a list of in-progress and completed transfers of
        funds in/out of any of the user's accounts.
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_gettransfers

        Args:
            params (dict):
            Parameter       Required    Type        Comments
            profile_id      no          str
            limit           no          int         number of results to return
            type            no          str         "deposit", "withdraw",
                                                    "internal_deposit", "internal_withdraw"
        """
        endpoint = "/transfers"
        return self._get(endpoint, params)

    ##############
    ### orders ###
    ##############

    def get_all_fills(self, params: Optional[Dict] = None):
        """
        Get a list of fills. A fill is a partial or complete match on a specific order.
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getfills

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            order_id    no          string      either order_id or product_id required
            product_id  no          string      either order_id or product_id required
            limit       no          int         default and max = 1000 rows
            after       no          str         pagination - use trade_id

        """
        endpoint = "/fills"
        return self._get(endpoint, params)

    ################
    ### products ###
    ################

    def get_product_candles(self, product_id: str, params: Optional[Dict] = None):
        """
        Historic rates for a product. Rates are returned in grouped buckets.
        Candle schema is of the form [timestamp, price_low, price_high, price_open, price_close]
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            granularity no          str         60, 300 seconds value
            start       no          str         timestamp
            end         no          str         timestamp
        """
        endpoint = f"/products/{product_id}/candles"
        return self._get(endpoint, params)

    def get_product_trades(self, product_id: str, params: Optional[Dict] = None):
        """
        Gets a list the latest trades for a product.
        https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproducttrades/

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            limit       no          int64       1000
            before      no          str         timestamp
            after       no          str         timestamp
        """
        endpoint = f"/products/{product_id}/trades"
        return self._get(endpoint, params)
