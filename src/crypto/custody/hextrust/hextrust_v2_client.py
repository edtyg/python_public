"""
https://hexsafe.gitbook.io/hex-safe-v2-rest-api-documentation
"""

import base64
import hashlib
import json
import os
import random
from datetime import datetime, timedelta

import jwt
import pandas as pd
import requests

from keys.api_work.custody.hextrust_v2 import HEXTRUST_V2


class hexsafe_v2:
    """
    Class to interact with hexsafe v2 APIs
    """

    def __init__(self, private_key: str, api_key: str):
        self.private_key = private_key
        self.api_key = api_key
        self.hexsafe_base_url = "https://api.hexsafe.hextrust.com"
        self.timeout = 3
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }

    #########################
    ### Auth Methods here ###
    #########################

    def gen_nonce(self) -> int:
        """
        Generates a random integer

        Returns:
            (int) 2647547864
        """
        return int(random.random() * 1e10)

    def gen_digest(self, body: str = "") -> str:
        """
        Function to generate digest

        Returns:
            (str) X83anO41yhueW9...
        """
        digest = hashlib.sha512()
        digest.update(body.encode())
        return base64.urlsafe_b64encode(digest.digest()).decode()

    def gen_jwt(self, private_key, api_key, method, uri, body=""):
        """
        Generates a json web token
        """
        nonce = self.gen_nonce()
        exp = datetime.now() + timedelta(days=1)
        claims = {
            "exp": int(exp.timestamp()),
            "api-key": api_key,
            "uri": uri,
            "nonce": nonce,
        }
        if method.lower() == "post":
            claims["digest"] = self.gen_digest(body)
        return jwt.encode(claims, private_key, algorithm="RS256")

    def send_request(self, method, uri, data):
        """send standard GET or POST requests"""
        jwt_token = self.gen_jwt(
            self.private_key,
            self.api_key,
            method,
            uri,
            json.dumps(data, indent=None, separators=(",", ":")) if data else "",
        )
        self.headers["Authorization"] = f"Bearer {jwt_token}"

        ### Get or Post ###
        if method.lower() == "get":
            print("GET Method")
            response = requests.get(
                self.hexsafe_base_url + uri,
                headers=self.headers,
                json=data,
                timeout=self.timeout,
            )
            return response.json()

        elif method.lower() == "post":
            print("POST Method")
            return None

        else:
            print("Invalid Method")
            return None

    ##########################
    ### hexsafe-v2 methods ###
    ##########################

    def get_safe_accounts(self, params: dict = None):
        """
        Get list of safe accounts
        Gets all safe accounts in an enterprise. This endpoint returns a paginated result.
        https://hexsafe.gitbook.io/hex-safe-v2-rest-api-documentation/hexsafe-api-reference/safe-accounts
        """
        uri = "/v1/safe_accounts"
        method = "get"
        data = self.send_request(method, uri, params)
        return data

    ### balance ###
    def main(self):

        mapping = {
            "btc:mainnet_BTC": "BTC",
            "1_ETH": "ETH",
            "1_USDT_0xdac17f95": "USDT",
            "1_USDC_0xA0b86991": "USDC",
        }

        data = self.get_safe_accounts()
        df_data = pd.DataFrame(data["safeAccountList"])

        df_final = pd.DataFrame()
        for i in df_data.index:
            wallet_name = df_data.loc[i, "name"]
            type = df_data.loc[i, "type"]
            asset_list = df_data.loc[i, "assetList"]
            if asset_list:
                df_asset_list = pd.DataFrame(asset_list)
                df_asset_list["type"] = type
                df_asset_list["wallet_name"] = wallet_name
                df_final = pd.concat([df_final, df_asset_list])
                # print(df_asset_list)

        df_final["mapped_tokens"] = df_final["assetKey"].map(mapping)
        return df_final


if __name__ == "__main__":
    save_path = os.path.dirname(os.path.realpath(__file__))
    pem_filename = "/my_rsa.pem"
    pem_filepath = save_path + pem_filename

    with open(pem_filepath, "r") as pem_file:
        pem_data = pem_file.read()
    client = hexsafe_v2(pem_data, HEXTRUST_V2["api_key"])

    bal = client.main()
    print(bal)
