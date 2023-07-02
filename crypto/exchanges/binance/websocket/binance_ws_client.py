"""
Binance Websocket Client
https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams
"""
import asyncio
import datetime as dt
import json

import pandas as pd
import websockets.client

# import nest_asyncio
# nest_asyncio.apply()


class BinanceWS:
    """Binance Websocket Client - for public requests only"""

    def __init__(self):
        self.base_endpoint = "wss://stream.binance.com:9443/ws/"

    async def ws_agg_trade_streams(self, symbol: str):
        """Websocket trade streams aggregated"""

        endpoint = self.base_endpoint + f"{symbol.lower()}@aggTrade"
        print(endpoint)

        async with websockets.client.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)

                data = {
                    "event_type": response["e"],
                    "event_time": response["E"],
                    "symbol": response["s"],
                    "aggregate_trade_id": response["a"],
                    "price": response["p"],
                    "qty": response["q"],
                    "first_trade_id": response["f"],
                    "last_trade_id": response["l"],
                    "trade_time": response["T"],
                    "maker_istrue": response["m"],
                    "placeholder": response["M"],
                }
                df_data = pd.DataFrame(data, index=[0])
                df_data["curr_time"] = dt.datetime.now()
                df_data.set_index("curr_time", inplace=True)
                print(df_data)

    async def ws_trade_streams(self, symbol: str):
        """Websocket trade streams"""

        endpoint = self.base_endpoint + f"{symbol.lower()}@trade"
        print(endpoint)

        async with websockets.client.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)

                data = {
                    "event_type": response["e"],
                    "event_time": response["E"],
                    "symbol": response["s"],
                    "trade_id": response["t"],
                    "price": response["p"],
                    "qty": response["q"],
                    "buyer_order_id": response["b"],
                    "seller_order_id": response["a"],
                    "trade_time": response["T"],
                    "maker_istrue": response["m"],
                    "placeholder": response["M"],
                }
                df_data = pd.DataFrame(data, index=[0])
                df_data["curr_time"] = dt.datetime.now()
                df_data.set_index("curr_time", inplace=True)
                print(df_data)

    async def ws_klines(self, symbol: str, interval: str):
        """Websocket kline streams
        intervals = 1s, 1m, 3m, 5m, 15m, 30m, 1h,
        2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        """

        endpoint = self.base_endpoint + f"{symbol.lower()}@kline_{interval}"
        print(endpoint)

        async with websockets.client.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                response_kline = response["k"]

                data = {
                    "event_time": response["E"],
                    "symbol": response["s"],
                    "kline_start_time": response_kline["t"],
                    "kline_close_time": response_kline["T"],
                    "interval": response_kline["i"],
                    "open": response_kline["o"],
                    "high": response_kline["h"],
                    "low": response_kline["l"],
                    "close": response_kline["c"],
                    "base_volume": response_kline["v"],
                    "quote_volume": response_kline["q"],
                }
                df_data = pd.DataFrame(data, index=[0])
                df_data["curr_time"] = pd.to_datetime(df_data["event_time"], unit="ms")
                df_data.set_index("curr_time", inplace=True)
                print(df_data)

    async def ws_orderbook_depth(self, symbol: str, depth: str):
        """Websocket orderbook data
        depth = 5, 10 or 20
        """

        endpoint = self.base_endpoint + f"{symbol.lower()}@depth{depth}"
        print(endpoint)

        async with websockets.client.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)

                df_data = pd.DataFrame(response)
                df_data["curr_time"] = dt.datetime.now()
                df_data.set_index("curr_time", inplace=True)
                print(df_data)


if __name__ == "__main__":
    client = BinanceWS()

    # asyncio.get_event_loop().run_until_complete(client.ws_agg_trade_streams("btcusdt"))
    # asyncio.get_event_loop().run_until_complete(client.ws_trade_streams("btcusdt"))
    asyncio.get_event_loop().run_until_complete(client.ws_klines("btcusdt", "1s"))
    # asyncio.get_event_loop().run_until_complete(client.ws_orderbook_depth("btcusdt", 5))
