"""
pip install websocket-client
"""

import websocket
import json


def on_open(ws):
    # send channel or auth here
    print("BINANCE Websocket connection opened")


def on_close(ws, close_status_code, close_msg):
    print("BINANCE Websocket connection closed")


def on_message(ws, message):
    # adjusting the output of the messages recevied
    # print(message) # raw message

    # u can adjust the message output here
    json_message = json.loads(message)  # converts message to dict format

    event = json_message["e"]
    event_time = json_message["E"]
    symbol = json_message["s"]
    price = json_message["p"]
    qty = json_message["q"]

    print(f"event = {event}")
    print(f"event_time = {event_time}")
    print(f"symbol = {symbol}")
    print(f"price = {price}")
    print(f"qty = {qty}")
    print("\n")


def on_error(ws, error):
    print(error)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        url="wss://stream.binance.com:9443/ws/btcbusd@trade",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
