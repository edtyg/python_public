"""
Websocket client for Deribit Exchange
"""

import asyncio
import json

import websockets

from keys.api_personal.crypto_exchanges.deribit import DERIBIT_READ


class deribitWebSocket:
    """
    Websocket client for deribit exchange
    private and public connections
    """

    def __init__(self, apikey: str, apisecret: str):
        self.deribit_ws_url = "wss://www.deribit.com/ws/api/v2"
        self.apikey = apikey
        self.apisecret = apisecret

        # send auth creds first for private websocket calls note id
        self.auth_creds = {
            "jsonrpc": "2.0",
            "id": 9929,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.apikey,
                "client_secret": self.apisecret,
            },
        }

    ##############
    ### public ###
    ##############

    async def get_trades_by_instrument(self, instrument_name: str, count: int):
        """
        Public Websocket connection
        Retrieve the latest trades that have occurred for a specific instrument.

        https://docs.deribit.com/?python#public-get_last_trades_by_instrument

        Args:
            Parameter           Required    Type    Description
            instrument_name     true        str     BTC-PERPETUAL
            count               false       int     number of items
        """
        async with websockets.connect(self.deribit_ws_url) as websocket:
            message = {
                "jsonrpc": "2.0",
                "id": 8772,
                "method": "public/get_last_trades_by_instrument",
                "params": {
                    "instrument_name": instrument_name,
                    "count": count,
                },
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    async def get_orderbook(self, instrument_name: str, depth: int):
        """
        Public Websocket connection
        Retrieves the order book, along with other market values for a given instrument.

        https://docs.deribit.com/?python#public-get_order_book

        Args:
            Parameter           Required    Type    Description
            instrument_name     true        str     BTC-PERPETUAL
            depth               false       int     number of items
        """
        async with websockets.connect(self.deribit_ws_url) as websocket:
            message = {
                "jsonrpc": "2.0",
                "id": 8772,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name,
                    "depth": depth,
                },
            }
            while websocket.open:
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print(response)

    ###############
    ### private ###
    ###############

    async def get_positions(self, currency: str, kind: str = None):
        """
        Public Websocket connection
        Retrieve user positions. To retrieve subaccount positions, use subaccount_id parameter.

        https://docs.deribit.com/?python#private-get_positions

        Args:
            Parameter       Required    Type    Description
            currency        true        str     BTC ETH USDC USDT
            kind            false       str     future option spot
        """
        async with websockets.connect(self.deribit_ws_url) as websocket:

            # login message
            await websocket.send(json.dumps(self.auth_creds))
            response = await websocket.recv()
            print("ws connection authenticated")

            while websocket.open:
                pos_msg = {
                    "jsonrpc": "2.0",
                    "id": 2236,
                    "method": "private/get_positions",
                    "params": {
                        "currency": currency,
                        "kind": kind,
                    },
                }
                await websocket.send(json.dumps(pos_msg))
                pos_response = await websocket.recv()
                pos_msg = json.loads(pos_response)
                print(pos_msg)


if __name__ == "__main__":
    account = DERIBIT_READ
    client = deribitWebSocket(account["api_key"], account["api_secret"])

    # asyncio.get_event_loop().run_until_complete(
    #     client.get_trades_by_instrument("ETH-PERPETUAL", 1)
    # )

    # asyncio.get_event_loop().run_until_complete(
    #     client.get_orderbook("ETH-PERPETUAL", 1)
    # )

    asyncio.get_event_loop().run_until_complete(client.get_positions("ETH", "future"))
