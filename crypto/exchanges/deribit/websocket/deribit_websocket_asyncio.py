import asyncio
import websockets
import json


async def call_dapi():
    async with websockets.connect("wss://test.deribit.com/ws/api/v2") as websocket:
        while True:
            msg = {
                "jsonrpc": "2.0",
                "method": "public/get_order_book",
                "id": 1,
                "params": {"instrument_name": "BTC-PERPETUAL"},
                "depth": "5",
            }
            await websocket.send(json.dumps(msg))

            response = await websocket.recv()
            response = json.loads(response)
            print(response)
            await asyncio.sleep(1)


asyncio.ensure_future(call_dapi())
asyncio.get_event_loop().run_forever()
