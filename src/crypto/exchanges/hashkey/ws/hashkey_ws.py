"""
API Docs here
sandbox environment available
https://hashkeypro-apidoc.readme.io/reference/websocket-api-1
"""

import asyncio
import websockets.client
import json

import nest_asyncio

nest_asyncio.apply()


class HashkeyWS:
    """
    Hashkey Exchange Websocket client
    """

    def __init__(self, api_key: str = None, api_secret: str = None):
        self.url = "wss://stream-pro.hashkey.com/quote/ws/v1"  # live endpoint
        self.client_id = api_key
        self.client_secret = api_secret

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
    async def kline_interval(self, symbol: str, interval: str):
        """
        getting klines

        Args:
            symbol  "BTCUSDT"
            interval "1m", "1h", "1d", ...
        """
        async with websockets.client.connect(self.url) as websocket:
            message = {
                "symbol": symbol,
                "topic": f"kline_{interval}",
                "event": "sub",
                "params": {"binary": False},
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def trades(self, symbol: str):
        """
        getting trades
        """
        async with websockets.client.connect(self.url) as websocket:
            message = {
                "symbol": symbol,
                "topic": "trade",
                "event": "sub",
                "params": {"binary": False},
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def depth(self, symbol: str):
        """
        getting orderbook depth
        """
        async with websockets.client.connect(self.url) as websocket:
            message = {
                "symbol": symbol,
                "topic": "depth",
                "event": "sub",
                "params": {"binary": False},
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)
                return response
                



if __name__ == "__main__":
    client = HashkeyWS()

    # while True:
    #     asyncio.get_event_loop().run_until_complete(
    #         client.kline_interval("BTCUSDT", "1M")
    #     )

    # while True:
    #     asyncio.get_event_loop().run_until_complete(client.trades("USDTUSD"))

    while True:
        asyncio.get_event_loop().run_until_complete(client.depth("USDTUSD"))
