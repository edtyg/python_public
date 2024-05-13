"""
OANDA API Docs here
https://developer.oanda.com/rest-live-v20/introduction/

Demo and Live account available
"""

from typing import Optional

import requests


class Oanda:
    """rest api for trading with Oanda broker
    use demo api key for demo env
    """

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.headers = {"Authorization": f"Bearer {self.apikey}"}
        self.timeout = 3

        self.base_url_live = "https://api-fxtrade.oanda.com"
        self.base_url_demo = "https://api-fxpractice.oanda.com"
        self.base_url = self.base_url_demo  # set to live endpoint

    ########################
    ### api call methods ###
    ########################

    def _get(self, endpoint: str):
        """get api call"""

        endpoint = self.base_url + endpoint
        response = requests.get(
            endpoint,
            headers=self.headers,
            timeout=self.timeout,
        )
        print(response.url)
        return response.json()

    ################
    ### Accounts ###
    ################

    # https://developer.oanda.com/rest-live-v20/account-ep/

    def get_accounts(self) -> dict:
        """
        Get a list of all accounts authorized for the provided token
        https://developer.oanda.com/rest-live-v20/account-ep/
        """
        endpoint = "/v3/accounts"
        return self._get(endpoint)

    def get_account_by_id(self, acc_id: str) -> dict:
        """
        Get the full details for a single account
        https://developer.oanda.com/rest-live-v20/account-ep/

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        endpoint = f"/v3/accounts/{acc_id}"
        return self._get(endpoint)

    def get_account_summary(self, acc_id: str) -> dict:
        """
        Get a summary for a single account
        https://developer.oanda.com/rest-live-v20/account-ep/

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        endpoint = f"/v3/accounts/{acc_id}/summary"
        return self._get(endpoint)

    def get_account_instruments(self, acc_id: str) -> dict:
        """
        Gets all tradeble instruments on your account - EUR_USD etc...
        https://developer.oanda.com/rest-live-v20/account-ep/

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        endpoint = f"/v3/accounts/{acc_id}/instruments"
        return self._get(endpoint)

    ##################
    ### Instrument ###
    ##################

    # https://developer.oanda.com/rest-live-v20/instrument-ep/

    def get_candles(self, instrument: str, params: Optional[dict] = None) -> dict:
        """Get candles for specific instrument

        Args:
            instrument (str): 'EUR_USD'

            params (Optional[dict], optional): Defaults to None.
            Name 	            Located In 	Type 	                Description
            price 	            query 	    PricingComponent 	    M, B, A [default = M]
            granularity 	    query 	    CandlestickGranularity 	S5,S10,S15,S30
                                                                    M1,M2,M4,M5,M10,M15,M30
                                                                    H1,H2,H3,H4,H6,H8,H12
                                                                    D W M
            count 	            query 	    integer 	            [default=500, maximum=5000]
            from 	            query 	    DateTime 	            timestamp
            to 	                query 	    DateTime 	            timestamp
            smooth 	            query 	    boolean 	            A smoothed ca
            includeFirst 	    query 	    boolean
            dailyAlignment 	    query 	    integer
            weeklyAlignment 	query 	    WeeklyAlignment
        """
        response = requests.get(
            self.base_url + f"/v3/instruments/{instrument}/candles",
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        print(response.url)
        return response.json()

    def get_orderbook(self, instrument: str) -> dict:
        """Get orderbook data from specific instrument

        Args:
            instrument (str): 'EUR_USD'
        """
        response = requests.get(
            self.base_url + f"/v3/instruments/{instrument}/orderBook",
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    def get_positionbook(self, instrument: str) -> dict:
        """_summary_

        Args:
            instrument (str): 'EUR_USD'
        """
        response = requests.get(
            self.base_url + f"/v3/instruments/{instrument}/positionBook",
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    #############
    ### Order ###
    #############

    def post_order(self, acc_id: str, order_info: dict) -> dict:
        """placing orders

        Args:
            acc_id (str): _description_
            order_info: (dict):
                 name        type        description
                 units       str         number of units
                 instrument  str         instrument name
                 timeinForce str         FOK, GTC
                 type        str         MARKET or LIMIT
                 price       str         price (not needed if market order)

        Returns:
            dict: _description_
        """
        response = requests.post(
            self.base_url + f"/v3/accounts/{acc_id}/orders",
            headers=self.headers,
            json=order_info,
            timeout=self.timeout,
        )
        return response.json()

    def get_account_orders(self, acc_id: str) -> dict:
        """Get current open orders for account

        Args:
            acc_id (str): _description_

        Returns:
            dict: _description_
        """
        base_url = self.base_url
        endpoint = f"/v3/accounts/{acc_id}/orders"

        response = requests.get(
            base_url + endpoint, headers=self.headers, timeout=self.timeout
        )
        data = response.json()
        return data
