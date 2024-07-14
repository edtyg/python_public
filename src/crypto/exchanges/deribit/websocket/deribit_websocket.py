import asyncio
import json
import time

import websockets

from local_credentials.api_key_exchanges import DERIBIT_KEY, DERIBIT_SECRET


class deribit_websocket:
    def __init__(self, client_id: str, client_secret: str, live: bool = False):
        if not live:
            self.url = "wss://test.deribit.com/ws/api/v2"  # test endpoint
        elif live:
            self.url = "wss://www.deribit.com/ws/api/v2"  # live endpoint

        self.client_id = client_id
        self.client_secret = client_secret

        self.auth_creds = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        }
        self.test_creds()

    @staticmethod
    def async_loop(api, message):
        return asyncio.get_event_loop().run_until_complete(api(message))

    def test_creds(self):
        response = self.async_loop(
            self.authenticate_credentials, json.dumps(self.auth_creds)
        )
        if "error" in response.keys():
            raise Exception(f"Auth failed with error {response['error']}")
        else:
            print("Auth creds are good, it worked")

    async def authenticate_credentials(self, msg):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)

    ###

    async def public_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            while True:
                await websocket.send(json.dumps(msg))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def private_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps(self.auth_creds))
            while websocket.open:
                response = await websocket.recv()
                await websocket.send(msg)
                response = await websocket.recv()
                break
            return json.loads(response)


if __name__ == "__main__":
    client = deribit_websocket(DERIBIT_KEY, DERIBIT_SECRET, live=True)

    loop = asyncio.get_event_loop()
    message = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "public/auth",
        "params": {
            "grant_type": "client_credentials",
            "client_id": DERIBIT_KEY,
            "client_secret": DERIBIT_SECRET,
        },
    }
    loop.run_until_complete(client.public_api(message))
