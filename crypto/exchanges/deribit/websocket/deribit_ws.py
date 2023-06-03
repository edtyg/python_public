import asyncio
import websockets
import json

# import nest_asyncio

# nest_asyncio.apply()
from local_credentials.api_key_exchanges import DERIBIT_KEY, DERIBIT_SECRET


class deribit_ws:
    def __init__(self, client_id: str, client_secret: str):
        self.url = "wss://www.deribit.com/ws/api/v2"  # live endpoint
        self.client_id = client_id
        self.client_secret = client_secret

        # send auth creds first for private websocket calls
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

    ### public websockets ###
    async def get_orderbook(self, instrument_name: str, depth: int):
        async with websockets.connect(self.url) as websocket:
            message = {
                "jsonrpc": "2.0",
                "id": 8772,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name,
                    "depth": depth,
                },
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    ### private websockets ###
    async def get_positions(self, currency: str, kind: str = None):
        async with websockets.connect(self.url) as websocket:
            auth_msg = {
                "jsonrpc": "2.0",
                "id": 9929,
                "method": "public/auth",
                "params": {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            }
            # login message
            await websocket.send(json.dumps(auth_msg))
            auth_response = await websocket.recv()

            while websocket.open:
                pos_msg = {
                    "jsonrpc": "2.0",
                    "id": 2236,
                    "method": "private/get_positions",
                    "params": {
                        "currency": currency,
                        # "kind" : kind,
                    },
                }
                await websocket.send(json.dumps(pos_msg))
                pos_response = await websocket.recv()
                pos_msg = json.loads(pos_response)
                print(pos_msg)


if __name__ == "__main__":
    client = deribit_ws(DERIBIT_KEY, DERIBIT_SECRET)

    asyncio.get_event_loop().run_until_complete(
        client.get_orderbook("ETH-PERPETUAL", 1)
    )
    # asyncio.get_event_loop().run_until_complete(client.get_positions('ETH'))
