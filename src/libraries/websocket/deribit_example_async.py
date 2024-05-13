"""
pip install websockets
"""

import json
import websockets
import asyncio

# import nest_asyncio

# nest_asyncio.apply()


async def get_order_book_price(symbol: str):
    """
    gets deribit orderbook
    """
    async with websockets.connect("wss://www.deribit.com/ws/api/v2") as websocket:
        msg = {
            "jsonrpc": "2.0",
            "method": "public/get_order_book",
            "id": 1,
            "params": {
                "instrument_name": symbol,
                "depth": "1",
            },
        }

        while True:
            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            response = json.loads(response)
            print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(get_order_book_price("BTC-PERPETUAL"))
