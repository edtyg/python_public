# rest apis for bitfinex
# https://docs.bitfinex.com/docs
# public api - get methods
# auth api - post methods

import hmac
import datetime as dt
import requests
import hashlib
from urllib.parse import urlencode
from typing import Optional, Dict
import json
from local_credentials.api_key_exchanges import BITFINEX_KEY, BITFINEX_SECRET


class bitfinex_rest:
    def __init__(self, apikey: str = None, apisecret: str = None):
        self.apikey = apikey
        self.apisecret = apisecret

        self.public_endpoints = (
            "https://api-pub.bitfinex.com/"  # base endpoint for public apis
        )
        self.auth_endpoints = (
            "https://api.bitfinex.com/"  # base endpoints for authenticated apis
        )

        # standard headers for signed api calls
        # would need to include time and signature as well
        # in get_signature method below

        self.headers = {
            "Content-Type": "application/json",
            "bfx-apikey": self.apikey,
        }

    def get_current_timestamp(self) -> str:
        """returns current timestamp - in milliseconds in string type

        Returns:
            str: _description_
        """
        ts = str(
            dt.datetime.now().timestamp() * 1000
        )  # current time in milliseconds, hence * 1000

        return ts

    def hashing(self, string: str) -> str:
        """
        hashes your string input - signed by your api secret key

        Args:
            query_string ([str]): [input is a string]

        Returns:
            [str]: [returns a hashed string, signed with api secret key]
        """
        final_string = hmac.new(
            self.apisecret.encode("utf-8"), string.encode("utf-8"), hashlib.sha384
        ).hexdigest()

        return final_string

    def get_signature(self, endpoint: str, params: Optional[Dict] = None):
        """
        Generates signature and adjusts the headers which will be used for your cals

        Args:
            endpoint ([str]): [endpoint for your api call] e.g. 'v2/auth/r/wallets'
            params (dict, optional): [input params if necessary, some api calls do not require params]
        """
        if params is None:
            final_params = ""
        else:
            final_params = json.dumps(params)

        nonce = self.get_current_timestamp()

        signature = f"/api/{endpoint}{nonce}{final_params}"
        print(signature)
        signed_signature = self.hashing(signature)

        # adjust headers for signed api calls
        self.headers["bfx-nonce"] = nonce
        self.headers["bfx-signature"] = signed_signature

    #################################################
    ### public api ###
    ### get methods ###
    ### 'https://api-pub.bitfinex.com/' ###

    def get_platform_status(self):
        """get status of bitfinex - 1 means working, 0 means not working
        https://docs.bitfinex.com/reference/rest-public-platform-status

        public api

        """

        base_url = self.public_endpoints
        endpoint = "v2/platform/status"

        response = requests.request("GET", base_url + endpoint)
        data = response.json()

        return data

    def get_tickers(self):
        """get all trading tickers available for bitfinex

        https://docs.bitfinex.com/reference/rest-public-tickers

        public api

        """

        base_url = self.public_endpoints
        endpoint = "v2/conf/pub:list:pair:exchange"

        response = requests.request("GET", base_url + endpoint)
        data = response.json()

        return data

    def get_book(self, symbol: str, params: dict):
        """get orderbook data

        https://docs.bitfinex.com/reference/rest-public-book

        public api

        params: ['len': 1] # 1, 25 or 100 for len
        """

        base_url = self.public_endpoints
        endpoint = f"v2/book/{symbol}/P0"

        response = requests.request("GET", base_url + endpoint, params=params)
        data = response.json()

        return data

    #################################################
    ### authenticated api ###
    ### post methods ###
    ### 'https://api.bitfinex.com/' ###

    def get_wallets(self, body: Optional[Dict] = None) -> list:
        """
        https://docs.bitfinex.com/reference/rest-auth-wallets
        Signed Request

        No Params needed for this api call

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
            WALLET_TYPE	            string	Wallet name (exchange, margin, funding)
            CURRENCY	            string	Currency (e.g. USD, ...)
            BALANCE	                float	Wallet balance
            UNSETTLED_INTEREST	    float	Unsettled interest
            AVAILABLE_BALANCE	    float	Wallet balance available for orders/withdrawal/transfer
            LAST_CHANGE	            string	Description of the last ledger entry
            TRADE_DETAILS	        object	If the last change was a trade, this object will show the trade details
        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/r/wallets"

        signature = self.get_signature(endpoint, body)

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def retrieve_orders(self, body: Optional[Dict] = None) -> list:
        """ retrieves all current open orders - or by specified order ids
        https://docs.bitfinex.com/reference/rest-auth-orders

        Signed Request
        Args:
            body (Optional[Dict], optional): takes in specific orders if you do not want the whole list
                 body = {'id': [id1, id2, id3]}. Defaults to None. put values in a list, value types = int

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
            ID	            int64	    Order ID
            GID	            int	        Group ID
            CID	            int	        Client Order ID
            SYMBOL	        string	    Pair (tBTCUSD, …)
            MTS_CREATE	    int	        Millisecond timestamp of creation
            MTS_UPDATE	    int	        Millisecond timestamp of update
            AMOUNT	        float	    Positive means buy, negative means sell.
            AMOUNT_ORIG	    float	    Original amount
            TYPE	        string	    The type of the order: LIMIT, EXCHANGE LIMIT, MARKET, EXCHANGE MARKET, STOP, \
                                                               EXCHANGE STOP, STOP LIMIT, EXCHANGE STOP LIMIT, TRAILING STOP, \
                                                               EXCHANGE TRAILING STOP, FOK, EXCHANGE FOK, IOC, EXCHANGE IOC.
            TYPE_PREV	    string	    Previous order type
            FLAGS	        int	        Active flags for order
            STATUS	        string	    Order Status: ACTIVE, PARTIALLY FILLED, RSN_PAUSE (trading is paused due to rebase events on AMPL or funding settlement on derivatives)
            PRICE	        float	    Price
            PRICE_AVG	    float	    Average price
            PRICE_TRAILING	float	    The trailing price
            PRICE_AUX_LIMIT	float	    Auxiliary Limit price (for STOP LIMIT)
            HIDDEN	        int	        1 if Hidden, 0 if not hidden
            PLACED_ID	    int	        If another order caused this order to be placed (OCO) this will be that other order's ID
            ROUTING	        string	    indicates origin of action: BFX, API>BFX
            META	        json string	Additional meta information about the order ( $F7 = IS_POST_ONLY (0 if false, 1 if true), $F33 = Leverage (int), aff_code: "aff_code_here")
        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/r/orders"

        signature = self.get_signature(endpoint, body)

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def submit_order(self, body: dict) -> list:
        """submit orders

        https://docs.bitfinex.com/reference/rest-auth-submit-order

        Signed Request
        Args:
            body (dict): takes in order infomation
            {
                type: 'LIMIT',
                symbol: 'tBTCUSD',
                price: '15',
                amount: '0.001', #Positive means buy, negative means sell.
                flags: 0, # https://docs.bitfinex.com/docs/flag-values - flag values here
                    Hidden	          int	64	    The hidden order option ensures an order does not appear in the order book; thus does not influence other market participants.
                    Close	          int	512	    Close position if position present.
                    Reduce Only	      int	1024	Ensures that the executed order does not flip the opened position.
                    Post Only	      int	4096	The post-only limit order option ensures the limit order will be added to the order book
                                                    and not match with a pre-existing order unless the pre-existing order is a hidden order.
                    OCO	              int	16384	The one cancels other order option allows you to place a pair of orders
                                                    stipulating that if one order is executed fully or partially,
                                                    then the other is automatically canceled.
                    No Var Rates	  int	524288	Excludes variable rate funding offers from matching against this order, if on margin
                    meta: {aff_code: "AFF_CODE_HERE"} // optional param to pass an affiliate code

              }

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/w/order/submit"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def update_order(self, body: dict) -> list:
        """update or adjust your current open order

        https://docs.bitfinex.com/reference/rest-auth-order-update

        Signed Request
        Args:
            body (dict): takes in order infomation
            {
                type: 'LIMIT',
                symbol: 'tBTCUSD',
                price: '15',
                amount: '0.001', #Positive means buy, negative means sell.
                flags: 0, # https://docs.bitfinex.com/docs/flag-values - flag values here
                    Hidden	          int	64	    The hidden order option ensures an order does not appear in the order book; thus does not influence other market participants.
                    Close	          int	512	    Close position if position present.
                    Reduce Only	      int	1024	Ensures that the executed order does not flip the opened position.
                    Post Only	      int	4096	The post-only limit order option ensures the limit order will be added to the order book
                                                    and not match with a pre-existing order unless the pre-existing order is a hidden order.
                    OCO	              int	16384	The one cancels other order option allows you to place a pair of orders
                                                    stipulating that if one order is executed fully or partially,
                                                    then the other is automatically canceled.
                    No Var Rates	  int	524288	Excludes variable rate funding offers from matching against this order, if on margin
                meta: {aff_code: "AFF_CODE_HERE"} // optional param to pass an affiliate code

              }

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/w/order/update"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def cancel_order(self, body: dict) -> list:
        """update or adjust your current open order

        https://docs.bitfinex.com/reference/rest-auth-cancel-order

        Signed Request
        Args:
            body (dict): takes in order infomation
            {
                type: 'LIMIT',
                symbol: 'tBTCUSD',
                price: '15',
                amount: '0.001', #Positive means buy, negative means sell.
                flags: 0, # https://docs.bitfinex.com/docs/flag-values - flag values here
                    Hidden	          int	64	    The hidden order option ensures an order does not appear in the order book; thus does not influence other market participants.
                    Close	          int	512	    Close position if position present.
                    Reduce Only	      int	1024	Ensures that the executed order does not flip the opened position.
                    Post Only	      int	4096	The post-only limit order option ensures the limit order will be added to the order book
                                                    and not match with a pre-existing order unless the pre-existing order is a hidden order.
                    OCO	              int	16384	The one cancels other order option allows you to place a pair of orders
                                                    stipulating that if one order is executed fully or partially,
                                                    then the other is automatically canceled.
                    No Var Rates	  int	524288	Excludes variable rate funding offers from matching against this order, if on margin
                meta: {aff_code: "AFF_CODE_HERE"} // optional param to pass an affiliate code

              }

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/w/order/cancel"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def order_history(self, symbol: str, body: Optional[dict] = None) -> list:
        """Get order history

        https://docs.bitfinex.com/reference/rest-auth-orders-history
        Data returned by this endpoint is limited to the past 3 months.
        For older data on your trading activity, please use the Trades endpoint.

        Signed Request
        Args:
            body (dict): takes in order infomation
            {
                'limit': 10, # number of rows of data
              }

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
        """

        base_url = self.auth_endpoints
        endpoint = f"v2/auth/r/orders/{symbol}/hist"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def get_trades(self, symbol: str, body: Optional[dict] = None) -> list:
        """Retrieve your trades.
        Your most recent trades will be retrieved by default,
        but a timestamp can be used to retrieve time-specific data.

        For trades before March 2020,
        the ORDER_TYPE field will not be populated as this data is not available.

        https://docs.bitfinex.com/reference/rest-auth-trades

        Signed Request
        Args:
            body (dict): takes in order infomation
            {
                'start': 1659682826000, # int millisecond start time
                'end': 1659682826001, # int millisecond end time
                'limit': 10, # int number of rows of data
                'sort': 1 or -1 # int 1 = ascending, -1 = descending
              }

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
        """

        base_url = self.auth_endpoints
        endpoint = f"v2/auth/r/orders/{symbol}/hist"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data

    def get_summary(self, body: Optional[Dict] = None) -> list:
        """account summary - fees mainly
        https://docs.bitfinex.com/reference/rest-auth-summary

        Signed Request
        Args:
            body (dict): takes in order infomation

        Returns:
            list: [response from api call - TERM, TYPE, DESCRIPTION]
            MAKER_FEE	        float	Shows the maker fee rate for the account
            DERIV_REBATE	    float	Shows the maker rebate for derivative trades on the account
            TAKER_FEE_TO_CRYPTO	float	Shows the taker fee rate for crypto to crypto trades on the account
            TAKER_FEE_TO_STABLE	float	Shows the taker fee rate for crypto to stable coin trades on the account
            TAKER_FEE_TO_FIAT	float	Shows the taker fee rate for crypto to fiat trades on the account
            DERIV_TAKER_FEE	    float	Shows the taker fee rate for derivative trades on the account
            LEO_LEV	            Int	    Shows the current LEO discount level of the account
            LEO_AMOUNT_AVG	    float	Shows the average amount of LEO held in the account over the past 30 days.

        """

        base_url = self.auth_endpoints
        endpoint = "v2/auth/r/summary"

        signature = self.get_signature(endpoint, body)  # this is to adjust the params

        response = requests.request(
            "POST", base_url + endpoint, headers=self.headers, json=body
        )
        data = response.json()

        return data


if __name__ == "__main__":
    client = bitfinex_rest(BITFINEX_KEY, BITFINEX_SECRET)

    # platform_status = client.get_platform_status()
    # tickers = client.get_tickers()
    # orderbook = client.get_book('tUSTUSD', 'R0', {'len': 25})

    # wallet = client.get_wallets()
    # open_orders = client.retrieve_orders()

    # order1 = client.submit_order(
    #     {
    #         'type': 'EXCHANGE LIMIT',
    #         'symbol': 'tUSTUSD',
    #         'price': '1.0050',
    #         'amount': '-3',
    #         'flags': 4096, # post only order
    #         }
    #     )

    # update_order1 = client.update_order(
    #     {
    #         'id': 101524427689,
    #         'price': '1.00050',
    #         'amount': '-2',
    #         'flags': 4096, # post only order
    #         }
    #     )

    # cancel_order1 = client.cancel_order(
    #       {
    #         'id': 101524427689,
    #         }
    #     )

    # order_history = client.order_history('tUSTUSD', {'limit':100})
    # trade_history = client.get_trades('tUSTUSD')
    # account_summary = client.get_summary()
