"""
deribit websocket connector
"""
import json
import pandas as pd
import websockets.client

from python.projects.deribit_trading.library_files.redis_client import RedisClient
from python.projects.deribit_trading.library_files.logger_client import LoggerClient
from python.projects.deribit_trading.library_files.keys import (
    API_KEY,
    API_SECRET_KEY,
)


class WebsocketPositions(RedisClient, LoggerClient):
    """
    Args:
        RedisClient (_type_): takes in redis client class
        LoggerClient (_type_): logging client class
    """

    def __init__(self, file_path, file_name, save_mode):
        RedisClient.__init__(self)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    async def get_positions(self, currency: str):
        """get account positions
        currency = 'BTC' or 'ETH'
        """
        tablename = f"DERIBIT_{currency}_POSITIONS"

        async with websockets.client.connect(
            "wss://www.deribit.com/ws/api/v2"
        ) as websocket:
            auth_msg = {
                "jsonrpc": "2.0",
                "id": 9929,
                "method": "public/auth",
                "params": {
                    "grant_type": "client_credentials",
                    "client_id": API_KEY,
                    "client_secret": API_SECRET_KEY,
                },
            }
            await websocket.send(json.dumps(auth_msg))
            auth_response = await websocket.recv()
            # uncomment here to check auth response, otherwise not needed
            # auth_response = json.loads(auth_response)
            print(auth_response)
            self.logger.info(auth_response)

            while True:
                pos_msg = {
                    "jsonrpc": "2.0",
                    "id": 2236,
                    "method": "private/get_positions",
                    "params": {
                        "currency": currency,
                    },
                }

                await websocket.send(json.dumps(pos_msg))
                pos_response = await websocket.recv()
                pos_msg = json.loads(pos_response)
                self.logger.info(pos_msg)

                timestamp = pos_msg["usOut"]
                data = pos_msg["result"]
                df_data = pd.DataFrame(data)

                df_data["timestamp"] = timestamp
                df_data["datetime"] = pd.to_datetime(df_data["timestamp"], unit="us")
                df_data.set_index("datetime", inplace=True)
                print(df_data)

                self.save_df(df_data, tablename)
                print("data saved to redis")
