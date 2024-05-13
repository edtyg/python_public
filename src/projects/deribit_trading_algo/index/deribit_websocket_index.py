"""
deribit websocket connector
"""
import json
import pandas as pd
import websockets.client

from python.projects.deribit_trading_algo.library_files.redis_client import RedisClient
from python.projects.deribit_trading_algo.library_files.logger_client import (
    LoggerClient,
)
from local_credentials.db_credentials import AFTERSHOCK_PC_MICRO_REDIS


class WebsocketIndex(RedisClient, LoggerClient):
    """
    Args:
        RedisClient (_type_): takes in redis client class
        LoggerClient (_type_): logging client class
    """

    def __init__(self, file_path, file_name, save_mode):
        RedisClient.__init__(self, AFTERSHOCK_PC_MICRO_REDIS)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    async def get_index_price(self, symbol_name: str):
        """
        Retrieves the current index price value for given index name.
        """
        tablename = f"DERIBIT_{symbol_name.upper()}_INDEX"

        async with websockets.client.connect(
            "wss://www.deribit.com/ws/api/v2"
        ) as websocket:
            msg = {
                "jsonrpc": "2.0",
                "method": "public/get_index_price",
                "id": 42,
                "params": {
                    "index_name": symbol_name,
                },
            }
            while True:
                await websocket.send(json.dumps(msg))
                response = await websocket.recv()
                response = json.loads(response)
                self.logger.info(response)

                data = response["result"]
                index_price = data["index_price"]
                timestamp = response["usOut"]

                data_dict = {
                    "timestamp": timestamp,
                    "index": symbol_name,
                    "index_price": index_price,
                }

                df_data = pd.DataFrame(data_dict, index=[0])
                df_data["datetime"] = pd.to_datetime(df_data["timestamp"], unit="us")
                df_data.set_index("datetime", inplace=True)

                self.save_df(df_data, tablename)
                print(df_data)
