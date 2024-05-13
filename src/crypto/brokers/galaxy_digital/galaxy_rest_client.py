"""
Galaxy rest client
"""
import base64
import hashlib
import hmac
import time
import urllib.parse

import pandas as pd
import requests
from local_credentials.api_key_brokers import GALAXY_KEY, GALAXY_SECRET


class GalaxyRest:
    """rest client"""

    def __init__(self, apikey: str, apisecret: str):
        self.base_url = "https://api.galaxydigital.io"
        self.apikey = apikey
        self.secret = apisecret
        self.headers = {}
        self.timeout = 10

    #################
    ### signature ###
    #################

    def get_signature(self, path: str, params: dict = None):
        """generates signature

        Args:
            path (str): _description_
            params (dict, optional): _description_. Defaults to None.
        """
        # path = api endpoint
        # body = params for api endpoint

        timestamp = str(int(time.time()))

        if params is None:
            message = timestamp + "GET" + path
        else:
            message = message = (
                timestamp + "GET" + path + "?" + urllib.parse.urlencode(params)
            )
        print(message)

        b_sec = base64.b64decode(self.secret)
        hashed = hmac.new(b_sec, message.encode(), hashlib.sha256)
        signature = base64.b64encode(hashed.digest()).decode()

        # setting standard headers
        self.headers["X-GD-KEY"] = self.apikey
        self.headers["X-GD-TIMESTAMP"] = timestamp
        self.headers["X-GD-SIGN"] = signature

    ###############
    ### methods ###
    ##############

    def get_health(self):
        """gets health of galaxy digital"""
        endpoint = "/health"
        self.get_signature(endpoint)
        response = requests.get(
            url=self.base_url + endpoint, headers=self.headers, timeout=self.timeout
        )
        return response.json()

    def get_balances(self):
        """gets balance"""
        endpoint = "/api/v1/balances"
        self.get_signature(endpoint)
        response = requests.get(
            url=self.base_url + endpoint, headers=self.headers, timeout=self.timeout
        )
        return response.json()

    def get_unsettled_orders(self, params: dict = None):
        """gets unsettled orders
        somehow also included orders that are settled

        Args:
            params (dict, optional):
                Field       Description                             Required
                size        Size of page (default 100, max 200)     Optional
                page        Number of page (0 indexed)              Optional
                sort        <FIELDNAME>, < asc | desc >             Optional
        """
        endpoint = "/api/v2/orders"
        self.get_signature(endpoint, params)
        response = requests.get(
            url=self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_order(self, order_id: str):
        """Get Trades for a given Order
        Args:
            params (dict, optional):
                Field       Description             Required
                id          The unique order Id.    Required
        """
        endpoint = f"/api/v2/orders/{order_id}/trades"
        self.get_signature(endpoint)
        response = requests.get(
            url=self.base_url + endpoint, headers=self.headers, timeout=self.timeout
        )
        return response.json()

    def get_historical_orders(self, params: dict = None):
        """gets unsettled orders
        Args:
            params (dict, optional):
                Field           Description
                fromDate        Orders (trade timestamp) starting from this day,
                                e.g 2021-02-11
                toDate          Orders (trade timestamp) up to and including this day,
                                e.g 2021-02-11
                fromDatetime    Orders (trade timestamp) starting from this datetime,
                                e.g 2021-02-11T20:00:00.000
                toDatetime      Orders (trade timestamp) up to this datetime,
                                e.g 2021-02-11T20:00:00.000
                size            Size of page (default 100, max 200)
                page            Number of page (0 indexed)
                sort            <FIELDNAME>,< asc | desc >
        """
        endpoint = "/api/v1/orders"
        self.get_signature(endpoint, params)
        response = requests.get(
            url=self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return response.json()

    def get_historical_order(self, order_id: str):
        """Get Trades for a given historical order
        Args:
            params (dict, optional):
                Field       Description             Required
                id          The unique order Id.    Required
        """
        endpoint = f"/api/v2/orders/historical/{order_id}/trades"
        self.get_signature(endpoint)
        response = requests.get(
            url=self.base_url + endpoint, headers=self.headers, timeout=self.timeout
        )
        return response.json()


if __name__ == "__main__":
    client = GalaxyRest(GALAXY_KEY, GALAXY_SECRET)

    # health = client.get_health()
    # print(health)

    balances = client.get_balances()
    print(balances)

    # unsettled_orders = client.get_unsettled_orders()
    # print(unsettled_orders)

    # order = client.get_order('56706140')
    # print(order)

    hist_orders = client.get_historical_orders()
    df_hist_orders = pd.DataFrame(hist_orders)
    print(df_hist_orders)

    # hist_order = client.get_historical_order('56706140')
    # print(hist_order)
