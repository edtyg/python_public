"""
B2C2 API docs
https://docs.b2c2.net/
login: counterparty
password: saINDIFECleAsTra

ip whitelist required
"""

from typing import Dict, Optional

import requests


class B2C2Rest:
    """_summary_"""

    def __init__(self, api_key: str):
        self.b2c2_base_endpoint = "https://api.b2c2.net"
        self.api_key = api_key
        self.headers = {"Authorization": f"Token {self.api_key}"}
        self.timeout = 3

    ###################
    ### API Methods ###
    ###################

    def _get(self, endpoint: str, params: Optional[Dict] = None):
        response = requests.get(
            self.b2c2_base_endpoint + endpoint,
            headers=self.headers,
            timeout=self.timeout,
            params=params,
        )
        return response.json()

    def _post(self, endpoint: str, params: Optional[Dict] = None):
        response = requests.post(
            self.b2c2_base_endpoint + endpoint,
            headers=self.headers,
            json=params,
            timeout=self.timeout,
        )
        return response.json()

    ######################
    ### b2c2 rest apis ###
    ######################

    def get_balances(self):
        """
        Get Balances
        https://docs.b2c2.net/#balances

        This shows the available balances in the supported currencies.
        Your account balance is the net result of all your trade and settlement activity.
        A positive number indicates that B2C2 owes you the amount of the given currency.
        A negative number means that you owe B2C2 the given amount.
        """
        endpoint = "/balance/"
        return self._get(endpoint)

    def get_margin_requirements(self):
        """
        Get Margin Requirements
        https://docs.b2c2.net/#get-margin-requirements
        """
        endpoint = "/margin_requirements/"
        return self._get(endpoint)

    def get_open_positions(self):
        """
        Get Open Positions - CFD trading only
        https://docs.b2c2.net/#get-open-positions
        """
        endpoint = "/cfd/open_positions/"
        return self._get(endpoint)

    def get_tradable_instruments(self):
        """
        Get tradable instruments
        https://docs.b2c2.net/#get-tradable-instruments

        This endpoint returns the list of all the instruments you can trade.
        Please ask your sales representative if you want access to more instruments.
        """
        endpoint = "/instruments/"
        return self._get(endpoint)

    ###################
    ### orders here ###
    ###################

    def post_rfq(self, params: dict):
        """
        POST Request
        https://docs.b2c2.net/#post-a-request-for-quote

        Parameter	        Type	    Description
        client_order_id	    String	    A universally unique identifier that will be returned to you in the response.
        quantity	        String	    Quantity in base currency (maximum 4 decimals).
        side	            String	    Either 'buy' or 'sell'.
        instrument	        String	    Instrument as given by the /instruments/ endpoint.
        """
        endpoint = "/request_for_quote/"
        return self._post(endpoint, params)

    def post_order(self, params: dict):
        """
        POST Request
        https://docs.b2c2.net/#order

        Params: Dict
        Parameter	        Type	    Description
        client_order_id	    String	    A universally unique identifier that will be returned to you in the response.
        quantity	        String	    Quantity in base currency (maximum 4 decimals).
        side	            String	    Either 'buy' or 'sell'.
        instrument	        String	    Instrument as given by the /instruments/ endpoint.
        order_type	        String	    Only 'FOK' and 'MKT' accepted for now.
        price	            String	    Price at which you want the order to be executed. Only FOK.
        force_open	        Boolean	    If true, B2C2 will open a new contract instead of closing the existing ones.
        valid_until	        String	    Datetime field formatted "%Y-%m-%dT%H:%M:%S.%fZ".
        acceptable_slippage_in_basis_points	String [0,20]	Acceptable leeway in bps, between 0 and 20. Only FOK. (maximum 2 decimals)
        executing_unit	S   tring [50]	Tag that the customer can assign to an order to link it to client side logic. It's not required and it can be duplicated.
        """
        endpoint = "/v2/order/"
        return self._post(endpoint, params)

    def get_multiple_orders(self, params: Optional[Dict] = None):
        """
        GET Request
        https://docs.b2c2.net/#get-multiple-orders

        Get order history - either thru web gui or API
        """
        endpoint = "/order/"
        return self._get(endpoint, params)

    def get_multiple_trades(self, params: Optional[Dict] = None):
        """
        Get Trades
        https://docs.b2c2.net/#trade

        API endpoint to get trade fills
        """
        endpoint = "/trade/"
        return self._get(endpoint, params)

    def get_ledger(self, params: Optional[Dict] = None):
        """
        Get Ledger entries
        https://docs.b2c2.net/#ledger

        Parameter	        Type	    Description
        type                str         "trade", "transfer", "funding", "realised_pnl"
        limit               int         default 50, max 1000
        """
        endpoint = "/ledger/"
        return self._get(endpoint, params)

    def get_all_withdrawals(self):
        """
        Get all withdrawals
        https://docs.b2c2.net/#get-all-withdrawals
        """
        endpoint = "/withdrawal/"
        return self._get(endpoint)

    def get_currencies(self):
        """
        Get currencies
        https://docs.b2c2.net/#currencies

        Returns all currencies supported by B2C2 and the minimum trade sizes.
        Note that “long_only” means that your balance in this currency cannot be negative.
        """
        endpoint = "/currency/"
        return self._get(endpoint)

    def get_account_info(self):
        """
        Get account info
        https://docs.b2c2.net/#account-info

        Returns generic account information related to trading:
            current risk exposure,
            maximum risk exposure and maximum quantity allowed per trade.
            Note that the risk exposure can be computed by doing the
            sum of all of the negative balances in USD.
        """
        endpoint = "/account_info/"
        return self._get(endpoint)
