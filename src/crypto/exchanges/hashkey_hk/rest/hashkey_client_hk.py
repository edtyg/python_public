"""
API Docs here
sandbox environment available
https://hashkeypro-apidoc.readme.io/reference/preparations
"""

import datetime as dt
import hashlib
import hmac
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


class HashkeyExchange:
    """
    Hashkey Exchange Authentication Parent class
    """

    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            "X-HK-APIKEY": self.api_key,
            "accept": "application/json",
        }
        self.recvwindow = 5000
        self.hashkey_base_url = "https://api-pro.hashkey.com"  # hk exchange
        self.timeout = 3

    ##############################
    ### authentication methods ###
    ##############################

    def get_current_timestamp(self) -> int:
        """
        gets current timestamp in milliseconds
        """
        timestamp = dt.datetime.now().timestamp() * 1000
        return int(timestamp)

    def get_signature(self, message: str) -> str:
        """
        signs message with api secret
        """
        final_string = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return final_string

    def get_query_string(self, params: Optional[Dict] = None) -> str:
        """
        sets up url params with signature for signed api calls
        """
        if params is None:
            params = {}

        query_string = urlencode(params, True)
        if query_string:
            query_string = (
                query_string
                + f"&recvWindow={self.recvwindow}"
                + f"&timestamp={self.get_current_timestamp()}"
            )
        else:
            query_string = (
                f"recvWindow={self.recvwindow}"
                + f"&timestamp={self.get_current_timestamp()}"
            )
        signature = self.get_signature(query_string)
        final_string = query_string + "&signature=" + signature
        return final_string

    ####################
    ### signed calls ###
    ####################

    ### get requests ###
    def _get_public(self, endpoint: str, params: Optional[Dict] = None) -> None:
        """public GET method"""
        response = requests.get(
            self.hashkey_base_url + endpoint,
            params=params,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    def _get_private(self, endpoint: str, params: Optional[Dict] = None) -> None:
        """signed GET method"""
        message = self.get_query_string(params)
        response = requests.get(
            self.hashkey_base_url + endpoint,
            params=message,
            headers=self.headers,
            timeout=self.timeout,
        )
        # print(response)
        return response.json()

    ### post requests ###
    def _post_signed(self, endpoint: str, params: Optional[Dict] = None) -> None:
        """signed POST method"""
        message = self.get_query_string(params)
        response = requests.post(
            self.hashkey_base_url + endpoint,
            params=message,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()

    ### delete requests ###
    def _delete_signed(self, endpoint: str, params: Optional[Dict] = None) -> None:
        """signed DELETE method"""
        message = self.get_query_string(params)
        response = requests.delete(
            self.hashkey_base_url + endpoint,
            params=message,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json()
