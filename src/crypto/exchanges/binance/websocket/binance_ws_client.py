"""
Binance Websocket Client
https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams
"""

import json

import websockets

# import nest_asyncio
# nest_asyncio.apply()


class BinanceWS:
    """Binance Websocket Client - for public requests only"""

    def __init__(self):
        self.binance_ws_base_endpoint = "wss://stream.binance.com:9443/ws/"

    async def aggregate_trade_stream(self, symbol: str):
        """
        The Aggregate Trade Streams push trade information that is aggregated
        for a single taker order.

        https://binance-docs.github.io/apidocs/spot/en/#aggregate-trade-streams
        """
        endpoint = self.binance_ws_base_endpoint + f"{symbol.lower()}@aggTrade"
        async with websockets.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def trade_stream(self, symbol: str):
        """
        The Trade Streams push raw trade information; each trade has a unique
        buyer and seller.The Trade Streams push raw trade information;
        each trade has a unique buyer and seller.

        https://binance-docs.github.io/apidocs/spot/en/#trade-streams
        """
        endpoint = self.binance_ws_base_endpoint + f"{symbol.lower()}@trade"
        async with websockets.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def klines(self, symbol: str, interval: str):
        """
        The Kline/Candlestick Stream push updates to the current
        klines/candlestick every second.

        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams

        intervals = 1s, 1m, 3m, 5m, 15m, 30m, 1h,
        2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        """
        endpoint = self.binance_ws_base_endpoint + f"{symbol.lower()}@kline_{interval}"
        async with websockets.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def orderbook(self, symbol: str, depth: str):
        """
        Top bids and asks, Valid are 5, 10, or 20.
        https://binance-docs.github.io/apidocs/spot/en/#individual-symbol-book-ticker-streams

        depth = 5, 10 or 20
        """
        endpoint = self.binance_ws_base_endpoint + f"{symbol.lower()}@depth{depth}"
        async with websockets.connect(endpoint) as websocket:
            while True:
                response = await websocket.recv()
                response = json.loads(response)
                print(response)


if __name__ == "__main__":
    client = BinanceWS()

    # asyncio.get_event_loop().run_until_complete(
    #     client.aggregate_trade_stream("btcusdt")
    # )

    # asyncio.get_event_loop().run_until_complete(client.trade_stream("btcusdt"))

    # asyncio.get_event_loop().run_until_complete(client.klines("btcusdt", "1m"))

    # asyncio.get_event_loop().run_until_complete(client.orderbook("btcusdt", 5))
