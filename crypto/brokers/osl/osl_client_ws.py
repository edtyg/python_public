"""
https://docs.osl.com/reference/introduction
api docs
"""

import asyncio
import json
import websockets.client
from osl_client import OslClient
from local_credentials.api_key_brokers import OSL_KEY, OSL_SECRET

# import nest_asyncio
# nest_asyncio.apply()


class OslClientWs(OslClient):
    """OSL Websocket client"""

    ####################
    ### brokerage WS ###
    ####################

    def auth_token(self):
        """gets token required for ws calls"""
        # https://docs.osl.com/reference/request-authentication-token
        body = {}

        method = "POST"
        path = "api/3/bcg/rest/auth/token"

        self.v3_mk_request(method, path, body)
        data = self.v3_mk_request(method, path, body)

        token = data["token"]
        return token

    async def get_order_book_price(self, instrument: str, currency: str):
        """subscribe to OSL price feeds
        instrument = "BTC.USD"
        currency = "BTC
        """
        token = self.auth_token()
        print(token)

        async with websockets.client.connect(
            f"wss://rfs.osl.com/bcg/ws/ws-client?token={token}"
        ) as websocket:
            msg = {
                "messageType": "subscribe",
                "instrument": instrument,
                "tag": "For future use",
                "quantity": 1,
                "currency": currency,
            }
            await websocket.send(json.dumps(msg))
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)


if __name__ == "__main__":
    client = OslClientWs(OSL_KEY, OSL_SECRET)

    while True:
        asyncio.get_event_loop().run_until_complete(
            client.get_order_book_price(instrument="BTC.USD", currency="BTC")
        )
