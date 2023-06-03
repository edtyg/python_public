"""
OKX V5 API
https://www.okx.com/docs-v5/en/#overview
"""
import base64
import datetime as dt
import hmac
import json
from urllib.parse import urlencode

import requests

from local_credentials.api_key_exchanges import OKX_KEY, OKX_SECRET, OKX_PASSPHRASE


class Okx:
    """Rest APIs for okx v5"""

    def __init__(self, apikey: str, apisecret: str, passphrase: str):
        self.apikey = apikey
        self.apisecret = apisecret
        self.passphrase = passphrase
        self.timeout = 5

        self.base_url = "https://www.okx.com"
        self.headers = {
            "OK-ACCESS-KEY": self.apikey,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "CONTENT-TYPE": "application/json",
        }

    ######################
    ### Authentication ###
    ######################

    def get_current_timestamp(self) -> str:
        """gets current timestamp with millisecond ISO format
        e.g. 2020-12-08T09:08:57.715Z
        """
        curr_time_utc = dt.datetime.utcnow()
        curr_time_utc_iso = curr_time_utc.isoformat("T", "milliseconds")
        timestamp_iso = curr_time_utc_iso + "Z"
        return timestamp_iso

    def sign(self, message: str):
        """signing of message with secret key"""
        secret_bytes = bytes(self.apisecret, encoding="utf8")
        message_bytes = bytes(message, encoding="utf8")

        signature_hash = hmac.new(
            secret_bytes,
            message_bytes,
            digestmod="sha256",
        )
        signature_digest = signature_hash.digest()
        return base64.b64encode(signature_digest)

    def hashing(self, request_type: str, endpoint: str, params: dict = None) -> str:
        """setting up headers for requests
        some slight differences for post and get requests for okx

        Args:
            request_type (str): "GET" or "POST" must be in caps
            endpoint (str): '/api/v5/account/balance?ccy=BTC' with params
            params (dict, optional): Defaults to None.

        Returns:
            str: _description_
        """
        timestamp = self.get_current_timestamp()

        if request_type.upper() == "GET" and params is None:
            message = timestamp + "GET" + endpoint

        elif request_type.upper() == "GET" and params is not None:
            message = timestamp + "GET" + endpoint + "?" + urlencode(params)

        elif request_type.upper() == "POST" and params is None:
            message = timestamp + "POST" + endpoint

        elif request_type.upper() == "POST" and params is not None:
            message = timestamp + "POST" + endpoint + json.dumps(params)

        data = self.sign(message)
        self.headers["OK-ACCESS-SIGN"] = data
        self.headers["OK-ACCESS-TIMESTAMP"] = timestamp

    ###############
    ### methods ###
    ###############

    # trade methods.
    def place_order(self, params: dict):
        """Place order
        https://www.okx.com/docs-v5/en/#rest-api-trade-place-order

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instId      String  Yes         instrument id e.g. BTC-USDT
            tdMode      String  Yes         Trade mode e.g. cash
            clOrdId     String  No          client order ID - assigned by us
            tag         String  No          order tag
            side        String  Yes         buy or sell
            ordType     String  Yes         market, limit, post_only, fok, ioc
            sz          String  Yes         size - quantity to buy or sell
            px          String  Conditional only for limit, post_only, fok, ioc
        """
        request_type = "POST"
        endpoint = "/api/v5/trade/order"
        self.hashing(request_type, endpoint, params)
        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            data=json.dumps(params),
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def cancel_order(self, params: dict):
        """cancel order
        https://www.okx.com/docs-v5/en/#rest-api-trade-cancel-order

        Args:
            params (dict):
            Parameter   Type    Required    Description
            instId      String  Yes         instrument id e.g. BTC-USDT
            ordId       String  Cond        either ordId or clOrdId
            clOrdId     String  Cond        Client Order ID as assigned by the client
        """
        request_type = "POST"
        endpoint = "/api/v5/trade/cancel-order"
        self.hashing(request_type, endpoint, params)
        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers,
            data=json.dumps(params),
            timeout=self.timeout,
        )
        data = response.json()
        return data

    # funding methods
    def get_balance_funding(self, params: dict = None):
        """Get balance in trading account
        https://www.okx.com/docs-v5/en/#rest-api-funding-get-balance
        """
        request_type = "GET"
        endpoint = "/api/v5/asset/balances"
        self.hashing(request_type, endpoint, params)
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    # account methods
    def get_balance_trading(self, params: dict = None):
        """Get balance in trading account
        https://www.okx.com/docs-v5/en/#rest-api-account-get-balance
        """
        request_type = "GET"
        endpoint = "/api/v5/account/balance"
        self.hashing(request_type, endpoint, params)
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data

    def get_positions(self, params: dict = None):
        """Get positions
        https://www.okx.com/docs-v5/en/#rest-api-account-get-positions
        """
        request_type = "GET"
        endpoint = "/api/v5/account/positions"
        self.hashing(request_type, endpoint, params)
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        data = response.json()
        return data


if __name__ == "__main__":
    client = Okx(OKX_KEY, OKX_SECRET, OKX_PASSPHRASE)

    account_balance_funding = client.get_balance_funding({"ccy": "BTC"})
    print(account_balance_funding)

    account_balance_trading = client.get_balance_trading({"ccy": "BTC"})
    print(account_balance_trading)

    # account_positions = client.get_positions()
    # print(account_positions)

    # order1 = client.place_order(
    #     {
    #         "instId": "BTC-USDT",
    #         "tdMode": "cash",
    #         "ordType": "limit",
    #         "side": "buy",
    #         "sz": "0.01",
    #         "px": "18000",
    #     }
    # )
    # print(order1)
