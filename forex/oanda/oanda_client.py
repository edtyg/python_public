"""
https://developer.oanda.com/rest-live-v20/introduction/
API Docs here
"""


from typing import Optional

import requests
from local_credentials.api_key_brokers import OANDA_KEY


class Oanda:
    """rest api for trading with Oanda broker"""

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.headers = {"Authorization": f"Bearer {self.apikey}"}
        self.base_url = "https://api-fxtrade.oanda.com"
        self.timeout = 5

    ################
    ### Accounts ###
    ################

    # https://developer.oanda.com/rest-live-v20/account-ep/

    def get_accounts(self) -> dict:
        """Gets the account numbers of all accounts you currently have"""
        response = requests.get(
            self.base_url + "/v3/accounts", headers=self.headers, timeout=self.timeout
        )
        return response.json()

    def get_account_by_id(self, acc_id: str) -> dict:
        """Gets account by ic

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        response = requests.get(
            self.base_url + f"/v3/accounts/{acc_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    def get_account_summary(self, acc_id: str) -> dict:
        """Gets account summary by id

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        response = requests.get(
            self.base_url + f"/v3/accounts/{acc_id}/summary",
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    def get_account_instruments(self, acc_id: str) -> dict:
        """Gets all tradeble instruments on your account - EUR_USD etc...

        Args:
            acc_id (str): '001-003-3456811-001'
        """
        response = requests.get(
            self.base_url + f"/v3/accounts/{acc_id}/instruments",
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

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


if __name__ == "__main__":
    client = Oanda(OANDA_KEY)
    accounts = client.get_accounts()
    print(accounts)

    # account
    ACCID = "001-003-3456811-001"
    account = client.get_account_by_id(ACCID)
    account_summary = client.get_account_summary(ACCID)
    account_instruments = client.get_account_instruments(ACCID)

    # instruments
    candles = client.get_candles("EUR_USD", {"granularity": "H1"})
    orderbook = client.get_orderbook("EUR_USD")
    positions = client.get_positionbook("EUR_USD")

    # orders
    # order_body = {
    #     "order": {
    #         "units": 100,
    #         "instrument": "EUR_USD",
    #         "timeinForce": "GTC",
    #         "type": "LIMIT",
    #         "price": 1.0000,
    #     }
    # }

    # order1 = client.post_order(acc_id, order_body)
    # acc_orders = client.get_account_orders(acc1_id)
