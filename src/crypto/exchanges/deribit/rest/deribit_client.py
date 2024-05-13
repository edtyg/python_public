"""
client to interact with deribit's api
"""

import base64
from typing import Dict, Optional

import requests


class DeribitRestClient:
    """
    A Python wrapper for the Deribit REST API.

    Args:
        apikey (str): The API key to authenticate requests.
        apisecret (str): The API secret to authenticate requests.
    """

    def __init__(self, apikey: str, apisecret: str):
        self.apikey = apikey
        self.apisecret = apisecret
        self.deribit_base_url = "https://www.deribit.com/api/v2"

        self.headers = {
            "Authorization": f'Basic {self.base64(self.apikey + ":" + self.apisecret)}'
        }
        self.timeout = 5

    def base64(self, message):
        """does a base64 encoding for your message"""
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return base64_message

    ### standard requests methods ###
    def _get(self, endpoint: str, params: Optional[Dict] = None):
        """standard get method"""
        response = requests.get(
            self.deribit_base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def _post(self, endpoint: str, params: Optional[Dict] = None):
        """standard get method"""
        response = requests.post(
            self.deribit_base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    ###################
    ### market data ###
    ###################

    def get_currencies(self):
        """
        Public method

        Retrieves all cryptocurrencies supported by the API.
        https://docs.deribit.com/?python#public-get_currencies
        """
        endpoint = "/public/get_currencies"
        return self._get(endpoint)

    def get_instruments(self, params: dict):
        """
        Public method

        Retrieves available trading instruments.
        This method can be used to see which instruments are available for
        trading, or which instruments have recently expired.
        https://docs.deribit.com/?python#public-get_instruments

        Args:
            params (dict):
            Parameter 	Required 	Type 	Enum
            currency 	true 	    string 	BTC, ETH, SOL, USDC
            kind        false       string  future, option, spot
            expired     false       boolean
        """
        endpoint = "/public/get_instruments"
        return self._get(endpoint, params)

    def get_order_book(self, params: dict):
        """
        Public method

        Retrieves the order book, along with other market values for
        a given instrument.
        https://docs.deribit.com/?python#public-get_order_book

        Args:
            params (dict):
            Parameter 	            Required 	Type
            instrument_name 	    true 	    str
            depth 	                false 	    int
        """
        endpoint = "/public/get_order_book"
        return self._get(endpoint, params)

    ###############
    ### trading ###
    ###############

    def place_buy_order(self, params: dict):
        """
        Private method

        Places a buy order for an instrument.
        https://docs.deribit.com/?python#private-buy

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name 	true 	    string
            amount              true        number
            type                false       string      limit, market
            label               false       string
            price               false       number
            time_in_force       false       string      good_til_cancelled
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/buy"
        return self._get(endpoint, params)

    def place_sell_order(self, params: dict):
        """
        Private method

        Places a sell order for an instrument.
        https://docs.deribit.com/?python#private-sell

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name 	true 	    string
            amount              true        number
            type                false       string      limit, market
            label               false       string
            price               false       number
            time_in_force       false       string      good_til_cancelled
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/sell"
        return self._get(endpoint, params)

    def edit_order(self, params: dict):
        """
        Private method

        Change price, amount and/or other properties of an order.
        https://docs.deribit.com/?python#private-edit

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            order_id         	true 	    string
            amount              true        number
            price               false       number
            post_only           false       boolean
            reduce_only         false       boolean
        """
        endpoint = "/private/edit"
        return self._get(endpoint, params)

    def cancel_order(self, params: dict):
        """
        Private method

        Cancel an order, specified by order id
        https://docs.deribit.com/?python#private-cancel

        Args:
            params (dict):
            Parameter 	        Required 	Type
            order_id         	true 	    string
        """
        endpoint = "/private/cancel"
        return self._get(endpoint, params)

    def get_order_state(self, params: dict):
        """
        Private method

        Retrieve the current state of an order.
        https://docs.deribit.com/?python#private-get_order_state

        Args:
            params (dict):
            Parameter 	        Required 	Type
            order_id         	true 	    string
        """
        endpoint = "/private/get_order_state"
        return self._get(endpoint, params)

    def get_user_trades_by_currency(self, params: dict):
        """
        Private method

        Retrieve the latest user trades that have occurred for
        instruments in a specific currency symbol.
        https://docs.deribit.com/?python#private-get_user_trades_by_currency

        Args:
            params (dict):
            Parameter 	Required 	Type
            currency 	true 	    string
            kind        false       string
            start_id    false       string
            end_id      false       string
            count       false       integer
            include_old false       boolean
            sorting     false       string
        """
        endpoint = "/private/get_user_trades_by_currency"
        return self._get(endpoint, params)

    def get_user_trades_by_instrument(self, params: dict):
        """
        Private method

        Retrieve the latest user trades that have
        occurred for a specific instrument.
        https://docs.deribit.com/?python#private-get_user_trades_by_instrument

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            instrument_name     true        string
            count               false       integer
            include_old         false       boolean
            sorting             false       string      asc, desc, default
        """
        endpoint = "/private/get_user_trades_by_instrument"
        return self._get(endpoint, params)

    ###############
    ### wallets ###
    ###############

    def get_deposits(self, params: dict):
        """
        Private method

        Retrieve the latest users deposits
        https://docs.deribit.com/?python#private-get_deposits

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """
        endpoint = "/private/get_deposits"
        return self._get(endpoint, params)

    def get_transfers(self, params: dict):
        """
        Private method

        Retrieve the user's transfers list
        https://docs.deribit.com/?python#private-get_transfers

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """
        endpoint = "/private/get_transfers"
        return self._get(endpoint, params)

    def get_withdrawals(self, params: dict):
        """
        Private method

        Retrieve the latest users withdrawals
        https://docs.deribit.com/?python#private-get_withdrawals

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        string      BTC,ETH,SOL,USDC
            count               false       integer
        """
        endpoint = "/private/get_withdrawals"
        return self._get(endpoint, params)

    ##########################
    ### account management ###
    ##########################

    def get_account_summary(self, params: str):
        """
        Private method

        Retrieves user account summary. To read subaccount summary use subaccount_id parameter.
        https://docs.deribit.com/?python#private-get_account_summary

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        str         BTC,ETH,SOL,USDC
            subaccount_id       false       int         sub acc user id
        """
        endpoint = "/private/get_account_summary"
        return self._get(endpoint, params)

    def get_positions(self, params: str):
        """
        Private method

        Retrieve user positions. To retrieve subaccount positions, use subaccount_id parameter.
        https://docs.deribit.com/?python#private-get_positions

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        str         BTC,ETH,SOL,USDC
            kind                false       str         future, option, spot
        """
        endpoint = "/private/get_positions"
        return self._get(endpoint, params)

    def get_transaction_log(self, params: str):
        """
        Private method

        Retrieve the latest user trades that have occurred for a specific instrument and within a given time range.
        https://docs.deribit.com/?python#private-get_transaction_log

        Args:
            params (dict):
            Parameter 	        Required 	Type 	    Enum
            currency            true        str         BTC,ETH,SOL,USDC
            start_timestamp	    true	    integer		The earliest timestamp to return result from 1613657734000
            end_timestamp	    true	    integer		The most recent timestamp to return result from 1613657734000
            query	            false	    string
            count	            false	    integer		Number of requested items, default - 100
            continuation	    false	    integer		Continuation token for pagination
        """
        endpoint = "/private/get_transaction_log"
        return self._get(endpoint, params)
