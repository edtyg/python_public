"""
binance api docs here
https://www.binance.com/en/binance-api
"""

import datetime as dt
import hashlib
import hmac
from typing import Dict, Optional
from urllib.parse import urlencode


class Binance:
    """
    Binance Rest API - Client for Authentication
    """

    def __init__(self, apikey: str = None, apisecret: str = None):
        self.apikey = apikey
        self.apisecret = apisecret
        self.headers = {"X-MBX-APIKEY": self.apikey}
        self.recvwindow = 10000
        self.url_timestamp = None

    def get_current_timestamp(self) -> int:
        """
        returns current timestamp in milliseconds
        """
        offset = 0  # pc time difference - use this to offset
        timestamp = int(dt.datetime.now().timestamp() - offset) * 1000
        return timestamp

    def hashing(self, query_string: str) -> str:
        """
        hashes string, signed by your api secret key

        Args:
            query_string ([str]): [input is a string]

        Returns:
            [str]: [returns a hashed string, signed with api secret key]

        Example:
            >>> query_string = "a=1&b=2&timestamp=123456789"
            >>> hashing(query_string)
            "f5a9c8a7b9d9f5e0f9f8f7f6f5f4f3f2f1f0f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
        """
        final_string = hmac.new(
            self.apisecret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return final_string

    def query_string(self, params: Optional[Dict] = None) -> str:
        """
        Takes in parameters needed for api call and sets them up for signed requests

        Args:
            params (dict, optional): [parameters for your api calls,
            some calls do not require params]

        Returns:
            [str]: [returns query string with timestamp appended at the end]
        """
        if params is None:
            params = {}

        # encode your params {'a':1, 'b':2} -> 'a=1&b=2'
        query_string = urlencode(params, True)

        if query_string:
            query_string = (
                query_string
                + "&timestamp="
                + str(self.get_current_timestamp())
                + f"&recvWindow={self.recvwindow}"
            )
        else:
            query_string = (
                "timestamp="
                + str(self.get_current_timestamp())
                + f"&recvWindow={self.recvwindow}"
            )
        return query_string

    def signed_request_url(
        self, base_url: str, endpoint: str, params: Optional[Dict] = None
    ) -> str:
        """
        Generates the url for the api call, requires base_url defined above & endpoint

        Args:
            base_url ([str]): [base url for spot, coinm or usdm]
            endpoint ([str]): [endpoint for your api call]
            params (dict, optional): [input params if necessary,
            some api calls do not require params]
        """
        if params is None:
            params = {}

        query_string = self.query_string(params)

        url = (
            base_url
            + endpoint
            + "?"
            + query_string
            + "&signature="
            + self.hashing(query_string)
        )
        self.url_timestamp = url
        return url
