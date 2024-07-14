"""
Coinbase Websocket Client
https://docs.cdp.coinbase.com/exchange/docs/websocket-overview/
"""

import asyncio
import json

import websockets


class CoinbaseWS:
    """Kraken Websocket Client - for public requests only"""

    def __init__(self):
        self.coinbase_ws_endpoint = "wss://ws-feed.exchange.coinbase.com"

    async def websocket_connector(self, connection_message: str):
        """
        generic websocket connector
        """
        while True:
            # outer loop to reconnect if ws is disconnected
            try:
                async with websockets.connect(self.coinbase_ws_endpoint) as websocket:
                    await websocket.send(json.dumps(connection_message))
                    while True:
                        # set while true to continuously receive ws feeds
                        try:
                            response = await websocket.recv()
                            response = json.loads(response)
                            print(response)

                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e}")

                        except websockets.ConnectionClosed as e:
                            print(f"Connection closed: {e}")
                            # exit inner loop
                            break

                        except Exception as error:
                            print(error)

            except websockets.WebSocketException as e:
                print(f"WebSocket exception: {e}")

            print("reconnecting")
            await asyncio.sleep(1)  # Delay before attempting to reconnect


if __name__ == "__main__":
    client = CoinbaseWS()

    connection_message = {
        "type": "subscribe",
        "product_ids": ["XRP-USD"],
        "channels": ["matches"],
    }

    asyncio.run(client.websocket_connector(connection_message))
