"""
Binance Websocket Client
https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams
"""

import asyncio
import json
import time

import websockets


class BinanceWS:
    """Binance Websocket Client - for public requests only"""

    def __init__(self):
        self.binance_ws = "wss://stream.binance.com:9443/ws"

    async def websocket_connector(self, connection_params: dict, runtime: int):
        """
        generic websocket connector

        Args:
            connection_params (dict): contains connect and disconnect params
            runtime (int): runtime in minutes
        """

        conn_start_time = time.time()
        conn_end_time = conn_start_time + 60 * runtime
        print(f"running ws conn for {runtime} minutes")

        connect_params = connection_params["connect"]
        disconnect_params = connection_params["disconnect"]

        while True:
            # outer loop to reconnect if ws is disconnected
            try:
                async with websockets.connect(self.binance_ws) as websocket:
                    # send connection params
                    print(f"sending connect params {connect_params}")
                    await websocket.send(json.dumps(connect_params))

                    while True:
                        # set while true to continuously receive ws feeds
                        try:
                            # preset run time
                            if time.time() > conn_end_time:
                                # sends disconnect params
                                print(f"sending disconnect params {disconnect_params}")
                                await websocket.send(json.dumps(disconnect_params))
                                break

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

                if time.time() > conn_end_time:
                    break

            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                await asyncio.sleep(1)

    async def trade_stream(self, symbol: str, runtime: int):
        """
        The Trade Streams push raw trade information;
        each trade has a unique buyer and seller.
        https://binance-docs.github.io/apidocs/spot/en/#trade-streams

        Args:
            symbol (str): btcusdt
            runtime (int): 1 = 1minute
        """
        params = {
            "connect": {
                "method": "SUBSCRIBE",
                "params": [f"{symbol.lower()}@aggTrade"],
                "id": 1,
            },
            "disconnect": {
                "method": "UNSUBSCRIBE",
                "params": [f"{symbol.lower()}@aggTrade"],
                "id": 312,
            },
        }
        await self.websocket_connector(params, runtime)

    async def kline(self, symbol: str, interval: str, runtime: int):
        """
        The Kline/Candlestick Stream push updates to the current klines/candlestick every second.
        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams

        Args:
            symbol (str): btcusdt
            interval (str): 1s, 1m, 1h ...
            runtime (int): 1 = 1minute
        """
        params = {
            "connect": {
                "method": "SUBSCRIBE",
                "params": [f"{symbol.lower()}@kline_{interval}"],
                "id": 1,
            },
            "disconnect": {
                "method": "UNSUBSCRIBE",
                "params": [f"{symbol.lower()}@kline_{interval}"],
                "id": 312,
            },
        }
        await self.websocket_connector(params, runtime)


if __name__ == "__main__":
    client = BinanceWS()

    asyncio.run(client.trade_stream("wldusdt", 0.2))
    # asyncio.run(client.kline("wldusdt", "1m", 0.2))
