import base64
import datetime as dt
import hashlib
import hmac
from typing import *
from urllib.parse import urlencode

import pandas as pd
import pytz
import requests

from local_credentials.api_key_exchanges import HUOBI_KEY, HUOBI_SECRET


class huobi:
    def __init__(self, apikey: str, apisecret: str):
        """_summary_

        Args:
            apikey (str): initialize with binance's api key
            apisecret (str): initialize with binance's secret key
        """
        self.apikey = apikey
        self.apisecret = apisecret

        self.spot_margin_url = "https://api.huobi.pro"  # spot and margin base url
        self.spot_margin_url_text = "api.huobi.pro"  # spot and margin base url

    ### methods for generating signed string for api calls ###

    def get_current_timestamp(self) -> str:
        date_time = dt.datetime.now(pytz.utc)  # current utc datetime
        date_string = date_time.strftime("%Y-%m-%dT%H:%M:%S")  # eg 2017-05-11T16:22:06

        return date_string

    def hashing(
        self, request_type: str, base_url_text: str, endpoint: str, query_string: str
    ) -> str:
        """
        hashes string, signed by your api secret key

        Args:
            request_type ([str]): [input = 'GET', 'POST']
            base_url_text ([str]): [input = api.huobi.pro, shortened version of base url]
            endpoint ([str]): [input = https://api.huobi.pro, base url]
            query_string ([str]): [input is a string]

        Returns:
            [str]: [returns a hashed string, signed with api secret key]
        """
        prepared_string = request_type + "\n" + base_url_text + "\n" + endpoint + "\n"
        final_string = prepared_string + query_string

        hash_code = hmac.new(
            self.apisecret.encode(), final_string.encode(), hashlib.sha256
        ).digest()
        signature = base64.b64encode(hash_code).decode()

        return signature

    def query_string(self, sort: bool, params: Optional[Dict] = None) -> str:
        """
        Takes in parameters needed for api call and sets them up for signed requests

        Args:
            sort ([bool]): [ if True, then sort dictionary, if False then do not sort]
            params (dict, optional): [parameters for your api calls, some calls do not require params]

        Returns:
            [str]: [returns query string]
        """
        if params is None:
            params = {}

        if sort == True:
            # fixed params - required params needed for signed calls
            fixed_params = {
                "AccessKeyId": self.apikey,
                "SignatureMethod": "HmacSHA256",
                "SignatureVersion": 2,
                "Timestamp": self.get_current_timestamp(),
            }

            fixed_params.update(
                params
            )  # adds in params that may or may not be required for the specific api call
            fixed_params = sorted(fixed_params.items())  # sort dictionary
            query_string_fixed = urlencode(fixed_params, True)

        else:
            fixed_params = {
                "AccessKeyId": self.apikey,
                "SignatureMethod": "HmacSHA256",
                "SignatureVersion": 2,
                "Timestamp": self.get_current_timestamp(),
            }

            fixed_params.update(
                params
            )  # adds in params that may or may not be required for the specific api call
            query_string_fixed = urlencode(fixed_params, True)

        return query_string_fixed

    def signed_request_url(
        self,
        request_type: str,
        base_url_text: str,
        base_url: str,
        endpoint: str,
        params: Optional[Dict] = None,
    ) -> str:
        """
        Generates the url for the api call, requires base_url defined above & endpoint

        Args:
            request_type ([str]): 'GET', 'POST'
            base_url_text ([str]): [input = api.huobi.pro, shortened version of base url]
            base_url ([str]): [base url for spot, coinm or usdm]
            endpoint ([str]): [endpoint for your api call]
            params (dict, optional): [input params if necessary, some api calls do not require params]
        """

        query_string_sorted = self.query_string(True, params)
        query_string_unsorted = self.query_string(False, params)

        url = (
            base_url
            + endpoint
            + "?"
            + query_string_sorted
            + "&Signature="
            + self.hashing(request_type, base_url_text, endpoint, query_string_unsorted)
        )

        return url

    #################################################
    ### api methods below ###
    ### Spot/Margin/Savings/Mining ###
    ### 'https://api.binance.com' ###

    def get_all_accounts(self) -> dict:
        """
        Signed Request

        No Params needed for this api call

        Returns:
            dict: contains account ids of various accounts (spot, otc, investment etc...)
        """

        request_type = "GET"
        base_url = self.spot_margin_url
        base_url_text = self.spot_margin_url_text
        endpoint = "/v1/account/accounts"

        url = self.signed_request_url(request_type, base_url_text, base_url, endpoint)

        response = requests.get(url)  # signed request
        data = response.json()

        return data

    def get_account_balance(self, account_id: float) -> dict:
        """
        Signed Request

        No Params needed for this api call

        Returns:
            dict: [response from api call]
        """

        request_type = "GET"
        base_url = self.spot_margin_url
        base_url_text = self.spot_margin_url_text
        endpoint = f"/v1/account/accounts/{account_id}/balance"

        url = self.signed_request_url(request_type, base_url_text, base_url, endpoint)

        response = requests.get(url)  # signed request
        data = response.json()

        return data


if __name__ == "__main__":
    client = huobi(HUOBI_KEY, HUOBI_SECRET)

    account_balance = client.get_account_balance(14636945)
    df = pd.DataFrame(account_balance["data"]["list"])
    print(account_balance)
