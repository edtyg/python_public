"""
asyncio - built in library in python
best used for concurrency and I/O-bound operations
works very well with websockets/requests
"""

import asyncio
import json

import websockets
from websockets.exceptions import ConnectionClosedError

# include this when running in spyder
# import nest_asyncio
# nest_asyncio.apply()


class DeribitWebsocket:
    """Example asyncio and WebSocket Deribit class"""

    def __init__(self):
        self.url = "wss://www.deribit.com/ws/api/v2"
        self.websocket = None

    async def on_open(self):
        """Message on opening connection"""
        print("Deribit WebSocket connection OPENED")

    async def on_close(self):
        """Message on closing connection"""
        print("Deribit WebSocket connection CLOSED")

    async def on_error(self, error_message):
        """Printing error messages"""
        print(f"Error Message: {error_message}")

    async def get_orderbook_stream(self, instrument_name: str):
        """WebSocket connection for Deribit orderbook data"""
        try:
            self.websocket = await websockets.connect(self.url)
            await self.on_open()
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
                await self.websocket.close()
        except ConnectionClosedError:
            await self.on_close()
        except Exception as error:
            await self.on_error(error)
        finally:
            if self.websocket is not None:
                await self.websocket.close()
                self.websocket = None


if __name__ == "__main__":
    client = DeribitWebsocket()
    # asyncio.run(get_orderbook_stream())
    # asyncio.run(get_orderbook_single_data())

    asyncio.get_event_loop().run_until_complete(
        client.get_orderbook_stream("ETH-PERPETUAL")
    )
    # asyncio.get_event_loop().run_until_complete(get_orderbook('ETH-PERPETUAL', 1))
