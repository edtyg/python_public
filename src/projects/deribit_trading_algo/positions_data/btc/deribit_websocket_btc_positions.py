"""
deribit websocket connector
"""
import asyncio
import os

from python.projects.deribit_trading.positions_data.deribit_websocket_positions import (
    WebsocketPositions,
)


if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "btc_positions.log"

    client = WebsocketPositions(save_path, FILENAME, "w")

    while True:
        asyncio.get_event_loop().run_until_complete(client.get_positions("BTC"))
