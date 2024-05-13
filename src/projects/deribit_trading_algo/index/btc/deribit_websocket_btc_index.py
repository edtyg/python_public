"""
deribit websocket connector
"""
import asyncio
import os

from python.projects.deribit_trading_algo.index.deribit_websocket_index import (
    WebsocketIndex,
)

if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "btc_usd_index.log"

    client = WebsocketIndex(save_path, FILENAME, "w")

    while True:
        asyncio.get_event_loop().run_until_complete(client.get_index_price("btc_usd"))
