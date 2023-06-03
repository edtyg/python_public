"""
BYBIT APIs
https://bybit-exchange.github.io/docs/v5/account/wallet-balance
"""

import datetime as dt
import hashlib
import hmac
from urllib.parse import urlencode

import requests

from local_credentials.api_key_exchanges import BYBIT_KEY, BYBIT_SECRET


class Bybit:
    """rest api for bybit"""

    def __init__(self, apikey: str, apisecret: str):
        self.base_url = "https://api.bybit.com"

        self.api_key = apikey
        self.api_secret = apisecret
        self.recv_window = str(5000)
        self.headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": None,
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": None,
            "X-BAPI-RECV-WINDOW": self.recv_window,
            "Content-Type": "application/json",
        }
        self.timeout = 5

    def get_current_timestamp(self):
        """gets current timestamp in milliseconds"""
        timestamp = str(int(dt.datetime.now().timestamp() * 1000))
        return timestamp

    def generate_signature(self, payload):
        """generates signature"""
        timestamp = self.get_current_timestamp()

        if payload is None:
            query_string = ""
        else:
            query_string = urlencode(payload, True)

        param_str = timestamp + self.api_key + self.recv_window + query_string
        hashing = hmac.new(
            bytes(self.api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256
        )
        signature = hashing.hexdigest()
        self.headers["X-BAPI-SIGN"] = signature
        self.headers["X-BAPI-TIMESTAMP"] = timestamp

    ###############
    ### Account ###
    ###############

    def get_wallet_balance(self, params: dict):
        """gets wallet balance

        Args:
            params (dict):
            Parameter   Required    Type        Comments
            accountType true        string      UNIFIED, CONTRACT, SPOT
        """
        base_endpoint = self.base_url
        endpoint = "/v5/account/wallet-balance"
        self.generate_signature(params)

        resp = requests.get(
            url=base_endpoint + endpoint,
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        return resp


if __name__ == "__main__":
    client = Bybit(BYBIT_KEY, BYBIT_SECRET)

    bal = client.get_wallet_balance({"accountType": "UNIFIED"})
    # z = client.post_upgrade_unified_margin()
    # print(bal.json())
