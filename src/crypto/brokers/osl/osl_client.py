"""
https://docs.osl.com/reference/introduction
api docs
"""

import time
import json
import base64
import hashlib
import hmac
import requests


class OslClient:
    """OSL client for authentication"""

    def __init__(self, apikey: str = None, apisecret: str = None):
        self.apikey = apikey
        self.apisecret = apisecret
        self.base_url = "https://trade-sg.osl.com"
        self.timeout = 5

        # headers for v3 api
        self.headers_v3 = {"Rest-Key": self.apikey}

    def gen_sig_helper(self, secret, data):
        """generate signature"""
        secret_bytes = base64.b64decode(secret.encode("utf8"))
        signature = base64.b64encode(
            hmac.new(
                secret_bytes, data.encode("utf8"), digestmod=hashlib.sha512
            ).digest()
        ).decode("utf8")
        return signature

    def v3_gen_sig(self, secret: str, path: str, body_str=None):
        """_summary_

        Args:
            apisecret (str): api secret key
            path (str): api/3/currencyStatic
            body_str (_type_, optional): _description_. Defaults to None.
        """

        data = path

        if body_str is not None:
            data = data + chr(0) + body_str

        signature = self.gen_sig_helper(secret, data)

        return signature

    def v3_mk_request(self, method: str, path: str, body: dict = None):
        """makes v3 requests"""
        if body is None:
            body = {}

        tonce = int(time.time() * 1000 * 1000)
        body["tonce"] = tonce
        body_str = json.dumps(body)

        self.headers_v3["Rest-Sign"] = self.v3_gen_sig(self.apisecret, path, body_str)
        self.headers_v3["Content-Type"] = "application/json"

        response = requests.request(
            method,
            self.base_url + "/" + path,
            headers=self.headers_v3,
            data=body_str,
            timeout=self.timeout,
        )
        response_json = response.json()
        return response_json
