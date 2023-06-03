# Spot Websockets
# https://bybit-exchange.github.io/docs/spot/v3/#t-websocket

import websocket
import json

## Public
# depth (orderbook) - https://bybit-exchange.github.io/docs/spot/v3/#t-websocketdepth
# trade - https://bybit-exchange.github.io/docs/spot/v3/#t-websockettrade
# kline - https://bybit-exchange.github.io/docs/spot/v3/#t-websocketkline
# tickers - https://bybit-exchange.github.io/docs/spot/v3/#t-websockettickers
# bookTicker - https://bybit-exchange.github.io/docs/spot/v3/#t-websocektbookticker

## Private
# outboundAccountinfo
# order
# stopOrder
# tickerinfo


channel_data = {
        'op': 'subscribe',
        'args': ['bookTicker.NFTUSDT']
        }
data = []

def on_open(ws):
    
    if channel_data:
        ws.send(json.dumps(channel_data))
    print("bybit connection opened")

def on_close(ws, close_status_code, close_msg):
    print("bybit connection closed")

def on_message(ws, message):
    
    json_message = json.loads(message) # converts string to dict format
    print(json_message) # raw message - string format
    data.append(json_message) # saves data
    
def on_error(ws, error):
    print(error)
    
    
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        url = 'wss://stream.bybit.com/spot/public/v3',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        )
    
    ws.run_forever()  # Set dispatcher to automatic reconnection
