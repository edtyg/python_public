import asyncio
import websockets
import json
from typing import Optional

# import nest_asyncio

# nest_asyncio.apply()


class binance_websocket:
    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "wss://stream.binance.com:9443/ws/"

    ### public websockets ###
    async def get_trade_streams(self, symbol: str):
        """get binance trade streams

        Args:
            instrument_name (str): btcusdt
        """
        url = self.base_url + f"{symbol}" + "@trade"
        print(url)
        async with websockets.connect(url) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)


if __name__ == "__main__":
    client = binance_websocket()
    asyncio.get_event_loop().run_until_complete(client.get_trade_streams("btcusdt"))
