"""
Whalefin (previously known as AMBER) api docs
https://pro.whalefin.com/apidoc/
"""

import datetime as dt
import hashlib
import hmac
import urllib.parse
from typing import Optional

import pandas as pd
import requests

from local_credentials.api_key_brokers import WHALEFIN_KEY, WHALEFIN_SECRET


class WhaleFin:
    """whalefin rest api"""

    def __init__(self, apikey: str, apisecret: str):
        self.apikey = apikey
        self.apisecret = apisecret
        self.url = "https://be.whalefin.com"
        self.headers = {"access-key": self.apikey}
        self.timeout = 5

    def get_timestamp(self) -> int:
        """get current timestamp in milliseconds"""
        timestamp = int(dt.datetime.now().timestamp() * 1000)
        return timestamp

    def get_headers(self, method: str, url_path: str, params_dict: dict) -> None:
        """Generates headers for api calls

        Args:
            method (str): either 'GET' or 'POST'
            url_path (str): api endpoint
            params_dict (dict): params if applicable
        """
        timestamp = self.get_timestamp()

        if params_dict is None:
            path = f"{url_path}"
        else:
            params = urllib.parse.urlencode(params_dict)
            path = f"{url_path}?{params}"

        sign_signature = f"method={method}&path={path}&timestamp={timestamp}"
        signature = hmac.new(
            self.apisecret.encode(), sign_signature.encode(), hashlib.sha256
        ).hexdigest()  # sign combine with apisecret

        self.headers["access-timestamp"] = str(timestamp)
        self.headers["access-sign"] = signature

    ################
    ### Asset v2 ###
    ################

    def get_account_statement(self, params: Optional[dict] = None) -> dict:
        """Gets account statement"""

        method = "GET"
        path = "/api/v2/asset/statement"

        self.get_headers(method=method, url_path=path, params_dict=params)

        response = requests.get(
            self.url + path,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_account_balance(self, params: Optional[dict] = None):
        """Get account balances

        Args:
            params (Optional[dict], optional): Defaults to None.
        """

        method = "GET"
        path = "/api/v2/asset/balance"

        self.get_headers(method=method, url_path=path, params_dict=params)

        response = requests.get(
            self.url + path,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    ###############
    ### Earn v2 ###
    ##############

    def get_list_earn_products(self, params: dict):
        """Gets a list of earn products

        Args:
            params (dict): * = required
            params  type    desc                            example
            *type   string  product type                    FIXED CUSTOMIZE
            ccy     string  currency of product             BTC ETH
            page    int     page number default = 1         1
            size    int     items per page default = 20     20

        """

        method = "GET"
        path = "/api/v2/earn/products"

        self.get_headers(method=method, url_path=path, params_dict=params)

        response = requests.get(
            self.url + path, headers=self.headers, params=params, timeout=self.timeout
        )
        data = response.json()
        return data

    def get_customized_earn_products(self, params: dict):
        """Gets cuztomized earn products
        yiels seem to be the same as locked products for same tenor

        Args:
            params (dict): * = required
            params  type    desc            example
            *id     string  product id      Evwesaf45sdgr32bosp
            *tenor  string  product tenor   10

        """

        method = "GET"
        path = "/api/v2/earn/products/customize-apr"

        self.get_headers(method=method, url_path=path, params_dict=params)

        response = requests.get(
            self.url + path, headers=self.headers, params=params, timeout=self.timeout
        )
        data = response.json()

        return data


if __name__ == "__main__":
    client = WhaleFin(WHALEFIN_KEY, WHALEFIN_SECRET)

    earn_prod = client.get_list_earn_products(
        {"type": "CUSTOMIZE", "size": 20, "page": 1}
    )
    df = pd.DataFrame(earn_prod["result"]["items"])

    cust_prod = client.get_customized_earn_products(
        {"id": "2XDAqZ4drwnytCbB46Ffe", "tenor": 1}
    )
