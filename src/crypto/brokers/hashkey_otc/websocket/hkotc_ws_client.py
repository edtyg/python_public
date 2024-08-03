"""
HashKey OTC Websocket Client
https://docs.hts.sg/
"""

import asyncio
import base64
import datetime as dt
import hashlib
import hmac
import json

import websockets

from keys.api_work.crypto_brokers.hashkey_otc import HASHKEY_OTC_TRADE


class HashKeyOTCWS:
    """Binance Websocket Client - for public requests only"""

    def __init__(self, apikey, apisecret):
        self.apikey = apikey
        self.apisecret = apisecret
        self.hkotc_ws = "wss://api.hts.sg/ws/private"

    ###########################
    ### Auth methods for WS ###
    ###########################

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

    def get_signature(self, timestamp: str, request_id: str) -> str:
        """
        Takes in parameters needed for api call and sets them up for signed requests

        Args:
            params (dict, optional): [parameters for your api calls,
            some calls do not require params]

        Returns:
            [str]: [returns query string with timestamp appended at the end]
        """
        "/v1/unify/quote?symbol=BTC- USDT"
        string_to_sign = timestamp + "GET" + "/ws/private?request_id=" + request_id
        query_string = self.hashing(string_to_sign)

        print(f"string to sign = {string_to_sign}")
        print(f"signed string = {query_string}")
        return query_string

    async def websocket_connector(self):
        """
        generic websocket connector

        Args:
            connection_params (dict): contains connect and disconnect params
            runtime (int): runtime in minutes
        """
        async with websockets.connect(self.hkotc_ws) as websocket:
            ts = self.get_current_timestamp()
            request_id = "test"
            signature = self.get_signature(ts, request_id)
            auth_params = {
                "operation": "auth",
                "request_id": request_id,
                "access_key": self.apikey,
                "timestamp": ts,
                "sign": signature,
            }
            print(auth_params)
            await websocket.send(json.dumps(auth_params))
            print("sent auth params")
            response = await websocket.recv()
            print(f"ws connection authenticated with response {response}")

            while websocket.open:
                subscribe_message = {
                    "operation": "sub_rts",
                    "request_id": request_id,
                    "symbol": "BTC-USD",
                    "side": "buy",
                    "target_size": "1",
                    "target_ccy": "base_ccy",
                }
                await websocket.send(json.dumps(subscribe_message))
                pos_response = await websocket.recv()
                pos_msg = json.loads(pos_response)
                print(pos_msg)


if __name__ == "__main__":
    key = HASHKEY_OTC_TRADE
    client = HashKeyOTCWS(key["api_key"], key["api_secret"])

    asyncio.run(client.websocket_connector())
