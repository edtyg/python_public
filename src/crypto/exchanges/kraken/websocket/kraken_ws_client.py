"""
Kraken Websocket Client
https://docs.kraken.com/api/docs/websocket-v2/add_order
"""

import asyncio
import json
import time

import websockets


class KrakenWS:
    """Kraken Websocket Client - for public requests only"""

    def __init__(self):
        self.kraken_ws_endpoint = "wss://ws.kraken.com/v2"

    async def websocket_connector(self, channel_params: str):
        """
        generic websocket connector
        """
        while True:
            # outer loop to reconnect if ws is disconnected
            try:
                async with websockets.connect(self.kraken_ws_endpoint) as websocket:
                    connection_message = {
                        "method": "subscribe",
                        "params": channel_params,
                    }
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

                        except KeyboardInterrupt:
                            print("Exiting gracefully...")
                            break

                        except Exception as error:
                            print(error)

            except websockets.WebSocketException as e:
                print(f"WebSocket exception: {e}")
                print("reconnecting")
                await asyncio.sleep(1)  # Delay before attempting to reconnect

            except KeyboardInterrupt:
                print("Exiting gracefully...")
                break


if __name__ == "__main__":
    client = KrakenWS()

    # params
    # ticker_params = {
    #     "channel": "ticker",
    #     "symbol": ["BTC/USD"]
    # }

    trade_params = {
        "channel": "trade",
        "symbol": ["BTC/USD", "ETH/USD"],
    }

    asyncio.run(client.websocket_connector(trade_params))
