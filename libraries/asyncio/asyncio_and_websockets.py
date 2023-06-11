"""
asyncio - built in library in python
best used for concurrency and I/O-bound operations
works very well with websockets/requests
"""

import asyncio
import json

import websockets

# include this when running in spyder
# import nest_asyncio
# nest_asyncio.apply()


class DeribitWebsocket:
    """Example asyncio and WebSocket Deribit class"""

    def __init__(self):
        self.url = "wss://www.deribit.com/ws/api/v2"
        self.websocket = None

    async def get_orderbook_stream(self, instrument_name: str):
        """WebSocket connection for Deribit orderbook data"""

        self.websocket = await websockets.connect(self.url)
        message = {
            "jsonrpc": "2.0",
            "id": 8772,
            "method": "public/get_order_book",
            "params": {
                "instrument_name": instrument_name,
                "depth": 1,
            },
        }
        while True:
            await self.websocket.send(json.dumps(message))
            response = await self.websocket.recv()
            print(response)


if __name__ == "__main__":
    client = DeribitWebsocket()
    asyncio.get_event_loop().run_until_complete(
        client.get_orderbook_stream("ETH-PERPETUAL")
    )
