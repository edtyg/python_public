# https://docs.ftx.com/reference/ticker-channel
# ftx websocket docs

import time
import hmac
import websocket
import json
from keys import *

class ftx_websocket:
    def __init__(self, api_key, api_secret):
        self.url = 'wss://ftx.com/ws/'
        self.api_key = api_key
        self.api_secret = api_secret
        
        self.channel_data = {}
        self.data = []
        
    def on_open(self, ws):
        print("FTX Connection Opened")
        if self.channel_data:
            ws.send(json.dumps(self.channel_data))
    
    def on_open_auth(self, ws):
        print("FTX Connection Opened")
        if self.channel_data:
            ws.send(json.dumps(self.authenticate()))
            ws.send(json.dumps(self.channel_data))

    def on_close(self, ws, close_status_code, close_msg):
        print("FTX connection Closed")

    def on_message(self, ws, message):
        
        json_message = json.loads(message)
        print(json_message)
        self.data.append(json_message)
        
    def on_error(self, ws, error):
        print(error)
        
    def authenticate(self):
        ts = int(time.time() * 1000)
        auth = {
            'op': 'login', 
            'args': {
                'key': self.api_key,
                'sign': hmac.new(self.api_secret.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest(),
                'time': ts,
                }
            }
        return(auth)
    
    ############################
    ### public websocket api ###
    ############################
    
    def ws_ticker(self, market: str):
        # The ticker channel provides the latest best bid and offer market data
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'ticker', 
            'market': market,
            }
        
        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()
        
    def ws_markets(self):
        # The markets channel provides information on the full set of tradable markets and their specifications.
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'markets', 
            }
        
        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()
    
    def ws_trades(self, market: str):
        # The trades channel provides data on all trades in the market
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'trades',
            'market': market
            }
        
        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()
    
    def ws_orderbook(self, market: str):
        # The orderbook channel provides data about the top 100 levels of the orderbook on either side
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'orderbook', 
            'market': market,
            }
        
        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()
    
    #############################
    ### private websocket api ###
    #############################
    
    def ws_fills(self):
        # The fills channel streams your fills across all markets.
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'fills', 
            }

        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open_auth,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()
    
    def ws_orders(self):
        # The orders channel streams updates to your orders across all markets.
        self.channel_data = {
            'op': 'subscribe', 
            'channel': 'orders', 
            }

        ws = websocket.WebSocketApp(
            url = self.url,
            on_open = self.on_open_auth,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            )
        ws.run_forever()

    
        
if __name__ == "__main__":
    client = ftx_websocket(ed_api_key, ed_api_secret)
    
    # client.ws_ticker('ETH/USD')
    # client.ws_markets()
    # client.ws_trades('ETH/USD')
    # client.ws_orderbook('ETH/USD')
    
    # client.ws_fills()
    # client.ws_orders()

