"""
HashKey OTC api docs here
https://qa-docs.hts.sg/
"""

import base64
import datetime as dt
import hashlib
import hmac
from typing import Dict, Optional
from urllib.parse import urlencode

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


class HashkeyOTC:
    """
    HashKey OTC - Authentication Client and error handling for requests
    """

    def __init__(self, apikey, apisecret):
        self.apikey = apikey
        self.apisecret = apisecret
        self.headers = {
            "HTS-ACCESS-KEY": self.apikey,
            "Content-Type": "application/json",
        }
        self.timeout = 5

    def get_current_timestamp(self) -> str:
        """
        Returns current timestamp in milliseconds in string type
        """
        timestamp = str(int(dt.datetime.now().timestamp()) * 1000)
        return timestamp

    def hashing(self, query_string: str) -> str:
        """
        hashes query_string, signed by your api secret key

        Args:
            query_string ([str]): [input is a string]

        Returns:
            [str]: [returns a hashed string, signed with api secret key]

        Example:
            >>> query_string = "a=1&b=2&timestamp=123456789"
            >>> hashing(query_string)
            "f5a9c8a7b9d9f5e0f9f8f7f6f5f4f3f2f1f0f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
        """
        signature = hmac.new(
            self.apisecret.encode(), query_string.encode(), hashlib.sha256
        ).digest()
        sign = base64.b64encode(signature).decode()
        return sign

    def get_signature(
        self, timestamp: int, method: str, endpoint: str, params: dict
    ) -> str:
        """
        Takes in parameters needed for api call and sets them up for signed requests

        Args:
            params (dict, optional): [parameters for your api calls,
            some calls do not require params]

        Returns:
            [str]: [returns query string with timestamp appended at the end]
        """
        if params is None:
            body = {}
        else:
            body = urlencode(params, True)
            # encode your params {'a':1, 'b':2} -> 'a=1&b=2'

        if body:
            string_to_sign = timestamp + method.upper() + endpoint + "?" + body
            query_string = self.hashing(string_to_sign)
        else:
            string_to_sign = timestamp + method.upper() + endpoint
            query_string = self.hashing(string_to_sign)

        print(f"string to sign = {string_to_sign}")
        print(f"signed string = {query_string}")
        return query_string

    #############################
    ### General Requests here ###
    #############################

    def rest_requests(
        self,
        method: str,
        base_url: str,
        endpoint: str,
        params: Optional[Dict] = None,
    ):
        """Rest requests with error handling
        Requests are all private

        Args:
            method (str): get, post, delete -> commonly used methods
            base_url (str): binance base url endpoint -> differs for spot, margin, futures
            endpoint (str): endpoint of your api call
            params (Optional[Dict]): params for your api call if required
        """

        if method.upper() not in ["GET", "POST", "DELETE", "PUT"]:
            print("Invalid Request Method")
            return

        try:
            curr_ts = self.get_current_timestamp()
            self.headers["HTS-ACCESS-TIMESTAMP"] = curr_ts
            self.headers["HTS-ACCESS-SIGN"] = self.get_signature(
                curr_ts, method, endpoint, params
            )

            if method.upper() == "GET":
                resp = requests.get(
                    base_url + endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                # print(resp.url)
            elif method.upper() == "POST":
                resp = requests.post(
                    base_url + endpoint,
                    json=params,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                print(resp.url)
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
