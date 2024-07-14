"""
binance api docs here
https://www.binance.com/en/binance-api
"""

import datetime as dt
import hashlib
import hmac
from typing import Dict, Optional
from urllib.parse import urlencode

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


class Binance:
    """
    Binance Rest API - Client for Authentication and error handling for requests
    """

    def __init__(self, apikey: str = None, apisecret: str = None):
        self.apikey = apikey
        self.apisecret = apisecret
        self.headers = {"X-MBX-APIKEY": self.apikey}
        self.recvwindow = 10000
        self.timeout = 5

    def get_current_timestamp(self) -> int:
        """
        returns current timestamp in milliseconds
        """
        offset = 0  # pc time difference - use this to offset if required
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

    ###############################
    ### URL for signed requests ###
    ###############################

    def signed_request_url(
        self,
        base_url: str,
        endpoint: str,
        params: Optional[Dict] = None,
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
        return url

    #############################
    ### General Requests here ###
    #############################

    def rest_requests(
        self,
        request_type: str,
        method: str,
        base_url: str,
        endpoint: str,
        params: Optional[Dict] = None,
    ):
        """Rest requests with error handling

        Args:
            request_type (str): either public or private api calls
            method (str): get, post, delete -> commonly used methods
            base_url (str): binance base url endpoint -> differs for spot, margin, futures
            endpoint (str): endpoint of your api call
            params (Optional[Dict]): params for your api call if required
        """

        if request_type.upper() not in ["PUBLIC", "PRIVATE"]:
            print("Invalid Request Type: has to be public or private")
            return

        if method.upper() not in ["GET", "POST", "DELETE", "PUT"]:
            print("Invalid Request Method")
            return

        try:
            if request_type.upper() == "PRIVATE":
                url = self.signed_request_url(base_url, endpoint, params)
                resp = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    timeout=self.timeout,
                )
            elif request_type.upper() == "PUBLIC":
                resp = requests.request(
                    method,
                    base_url + endpoint,
                    params=params,
                    timeout=self.timeout,
                )

            return resp.json()

        except HTTPError as http_error:
            # 404 or 500 error
            print(f"HTTP Error: {http_error}")

        except Timeout as timeout_error:
            # Request timed out
            print(f"Request Timed out: {timeout_error}")

        except RequestException as request_error:
            # Other requests error
            print(f"Request error: {request_error}")

        except ValueError as json_error:
            # Json decoding error
            print(f"JSON decode error: {json_error}")

        except Exception as error:
            # other exceptions
            print(f"An unexpected error occurred: {error}")
