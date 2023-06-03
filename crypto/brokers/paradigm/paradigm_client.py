"""
https://docs.paradigm.co/#paradigm-api
paradigm api docs
"""
import base64
import hmac
import json
import time
from typing import Optional
from urllib.parse import urlencode

import requests

from local_credentials.api_key_brokers import PARADIGM_KEY, PARADIGM_SECRET


class ParadigmClient:
    """paradigm client"""

    def __init__(self, apikey: str, apisecret: str):
        self.apikey = apikey
        self.apisecret = apisecret

        self.base_url = "https://api.chat.paradigm.co"
        self.base_url_fspd = "https://api.fs.chat.paradigm.co"
        self.timeout = 5
        self.headers = {"Authorization": f"Bearer {self.apikey}"}

    def set_headers(self, method: str, path: str, body: dict):
        """Get timestamp and signature then add it to headers

        Args:
            method (str): 'GET', 'POST', 'DELETE'
            path (str): endpoint e.g. /v1/fs/instruments
            body (params): params if any - if not = ''
        """

        signing_key = base64.b64decode(self.apisecret)  # api secret here
        timestamp = str(int(time.time() * 1000)).encode("utf-8")

        message = b"\n".join([timestamp, method.upper(), path, body])
        digest = hmac.digest(signing_key, message, "sha256")
        signature = base64.b64encode(digest)

        self.headers["Paradigm-API-Timestamp"] = timestamp
        self.headers["Paradigm-API-Signature"] = signature

    ################################################
    ### FSPD endpoints - Future Spread Dashboard ###
    ################################################

    # https://docs.paradigm.co/beta/index.html?python#fspd-rest-endpoints

    def get_fspd_instruments(self, params: Optional[dict] = None) -> dict:
        """Gets futures spreads instruments - id, name etc...

        https://docs.paradigm.co/#get-instruments-3

        Args:
            params(Optional) dict
            Name	                In	    Type	Required	Description
            cursor	                query	string	false	    Returns the next paginated page.
            venue	                query	string	false	    Values include DBT, BYB
            kind	                query	string	false	    ANY, FUTURE, SPOT.
            settlement_currency	    query	string	false	    Currency instrument is settled in.
            clearing_currency	    query	string	false	    Currency order size
            name	                query	string	false	    The name of the Instrument
            venue_instrument_name	query	string	false	    returned by the underlying venue.
            state	                query	string	false	    ACTIVE, SETTLED, EXPIRED.
            page_size	            query	string	false	    Default is to return all.
            margin_type	            query	string	false	    HLINEAR, INVERSE.
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = "/v1/fs/instruments"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_strategies(self, params: Optional[dict] = None) -> dict:
        """Gets futures spreads strategies - id, name etc...

        https://docs.paradigm.co/#get-strategies

        Args:
            params(Optional) dict
            Name	                In	    Type	Required	Description
            cursor	                query	string	false	    Returns the next paginated page.
            venue	                query	string	false	    Values include DBT, BYB
            kind	                query	string	false	    ANY, FUTURE, SPOT.
            settlement_currency	    query	string	false	    Currency instrument is settled in.
            clearing_currency	    query	string	false	    Currency order size
            name	                query	string	false	    The name of the Instrument
            venue_instrument_name	query	string	false	    returned by the underlying venue.
            state	                query	string	false	    ACTIVE, SETTLED, EXPIRED.
            page_size	            query	string	false	    Default is to return all.
            margin_type	            query	string	false	    HLINEAR, INVERSE.

        """

        base_url = self.base_url_fspd

        method = "GET"
        path = "/v1/fs/strategies"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_strategy_by_id(
        self, strategy_id: int, params: Optional[dict] = None
    ) -> dict:
        """Gets futures spreads strategies by id

        https://docs.paradigm.co/#get-strategies-strategy_id

        Args:
            params(Optional) dict
            Name            In	        Type	Required	Description
            strategy_id 	endpoint 	string 	true 	    unique identifier of the Strategy.
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = f"/v1/fs/strategies/{strategy_id}"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_strategy_orderbook(
        self, strategy_id: int, params: Optional[dict] = None
    ) -> dict:
        """Gets futures spreads orderbook by id

        https://docs.paradigm.co/#get-strategies-strategy_id-order-book

        Args:
            params(Optional) dict
            Name            In	        Type	Required	Description
            strategy_id 	endpoint 	string 	true 	    unique identifier of the Strategy.
            depth 	        query 	    string 	false 	    ALL, 1, 5, and 25.
            level 	        query 	    string 	false 	    L2, L3

        """

        base_url = self.base_url_fspd

        method = "GET"
        path = f"/v1/fs/strategies/{strategy_id}/order-book"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_strategy_orderbook_summary(
        self, strategy_id: int, params: Optional[dict] = None
    ) -> dict:
        """Gets futures spreads orderbook summary by id

        https://docs.paradigm.co/#get-strategies-strategy_id-order-book-summary

        Args:
            params(Optional) dict
            Name            In	        Type	Required	Description
            strategy_id 	endpoint 	string 	true 	    unique identifier of the Strategy.
            level 	        query 	    string 	false 	    L2, L3
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = f"/v1/fs/strategies/{strategy_id}/order-book-summary"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_orders(self, params: Optional[dict] = None) -> dict:
        """Gets futures spread orders

        https://docs.paradigm.co/#get-orders-2

        Args:
            params(Optional) dict
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = "/v1/fs/orders"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_fspd_orders_by_id(
        self, order_id: int, params: Optional[dict] = None
    ) -> dict:
        """Gets futures spread orders by id

        https://docs.paradigm.co/#get-orders-order_id-2

        Args:
            params(Optional) dict
            Name        In          Type	Required	Description
            order_id 	endpoint 	string 	true 	    unique identifier of the Order.

        Returns:
            dict:
                {'id': '58987290357137417',
                 'last_updated': 1665404871115439977,
                 'best_bid_price': '-0.30',
                 'best_bid_amount': 11420,
                 'best_bid_amount_decimal': '11420.5',
                 'best_ask_price': '-0.20',
                 'best_ask_amount': 1403,
                 'best_ask_amount_decimal': '1403.57',
                 'last_trade_amount': 33,
                 'last_trade_price': '-0.20',
                 'last_trade_amount_decimal': '33.849'}
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = f"/v1/fs/orders/{order_id}"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def post_order(self, payload: dict) -> dict:
        """Posts an order

        https://docs.paradigm.co/#post-orders

        Args:
            body (dict): body should include the following:
            NAME            IN      TYPE    REQUIRED    DESCRIPTION

        Returns:
            dict: _description_
        """

        base_url = self.base_url_fspd

        method = "POST"
        path = "/v1/fs/orders"

        body = json.dumps(payload)

        self.set_headers(method.encode(), path.encode(), body.encode())
        response = requests.post(
            base_url + path, headers=self.headers, json=payload, timeout=self.timeout
        )
        data = response.json()

        return data

    def post_replace_order(self, order_id: int, payload: dict) -> dict:
        """Updates an existing order

        https://docs.paradigm.co/#post-orders-order_id-replace

        Args:
            body (dict): body should include the following:
            Name	        In	        Type	Required	Description

        Returns:
            dict: _description_
        """

        base_url = self.base_url_fspd

        method = "POST"
        path = f"/v1/fs/orders/{order_id}/replace"

        body = json.dumps(payload)

        self.set_headers(method.encode(), path.encode(), body.encode())
        response = requests.get(
            base_url + path, headers=self.headers, json=payload, timeout=self.timeout
        )
        data = response.json()

        return data

    def delete_orders(self, params: Optional[dict] = None) -> dict:
        """Deletes all open orders - across all accounts

        https://docs.paradigm.co/#delete-orders

        Args:
            body (dict): body should include the following:
            Name    In	    Type	Required	Description
            side 	query 	string 	false 	    Valid values include BUY and SELL.
            label 	query 	string 	false 	    label of all Orders to Cancel.

        Returns:
            dict: _description_
        """

        base_url = self.base_url_fspd

        method = "DELETE"
        path = "/v1/fs/orders"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def delete_orders_by_id(self, order_id: int, params: Optional[dict] = None) -> dict:
        """Deletes all open orders - across all accounts

        https://docs.paradigm.co/#delete-orders-order_id

        Args:
            body (dict): body should include the following:
            Name	    In	        Type	Required	Description
            order_id 	endpoint 	string 	true 	    order_id of the Order to Cancel.

        Returns:
            dict: _description_
        """

        base_url = self.base_url_fspd

        method = "DELETE"
        path = f"/v1/fs/orders/{order_id}"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data

    def get_trades(self, params: Optional[dict] = None) -> dict:
        """Gets trades

        https://docs.paradigm.co/#get-trades-3

        Args:
            params(Optional) dict
            Name                In      Type	Required	Description
        """

        base_url = self.base_url_fspd

        method = "GET"
        path = "/v1/fs/trades"
        body = ""

        if params:
            final_path = path + "?" + urlencode(params)
        else:
            final_path = path

        self.set_headers(method.encode(), final_path.encode(), body.encode())
        response = requests.get(
            base_url + final_path, headers=self.headers, timeout=self.timeout
        )
        data = response.json()

        return data


if __name__ == "__main__":
    client = ParadigmClient(PARADIGM_KEY, PARADIGM_SECRET)
    instruments = client.get_fspd_instruments({"venue": "BYB"})
