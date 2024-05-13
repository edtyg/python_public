"""
deribit websocket connector
"""
import asyncio
import os

from python.projects.deribit_trading.orderbook_data.deribit_websocket_orderbook import (
    WebsocketOrderbook,
)

if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "eth_usd_orderbook.log"

    client = WebsocketOrderbook(save_path, FILENAME, "w")

    while True:
        asyncio.get_event_loop().run_until_complete(
            client.get_order_book_price("ETH-PERPETUAL")
        )
