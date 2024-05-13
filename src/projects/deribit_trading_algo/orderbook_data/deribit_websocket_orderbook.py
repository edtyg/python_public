"""
deribit websocket connector
"""
import json
import pandas as pd
import websockets.client

from python.projects.deribit_trading.library_files.redis_client import RedisClient
from python.projects.deribit_trading.library_files.logger_client import LoggerClient


class WebsocketOrderbook(RedisClient, LoggerClient):
    """
    Args:
        RedisClient (_type_): takes in redis client class
        LoggerClient (_type_): logging client class
    """

    def __init__(self, file_path, file_name, save_mode):
        RedisClient.__init__(self)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    async def get_order_book_price(self, symbol: str):
        """subscribe to price feeds level 1 = top of orderbook
        symbol = 'BTC/USD' for example
        """
        tablename = f"DERIBIT_{symbol}_ORDERBOOK"

        async with websockets.client.connect(
            "wss://www.deribit.com/ws/api/v2"
        ) as websocket:
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
                self.logger.info(response)

                data = response["result"]
                timestamp = data["timestamp"]
                bid = data["bids"][0][0]
                ask = data["asks"][0][0]

                data_dict = {
                    "timestamp": timestamp,
                    "bid": bid,
                    "ask": ask,
                }
                df_data = pd.DataFrame(data_dict, index=[0])
                df_data["datetime"] = pd.to_datetime(df_data["timestamp"], unit="ms")
                df_data.set_index("datetime", inplace=True)

                self.save_df(df_data, tablename)
                print(df_data)
