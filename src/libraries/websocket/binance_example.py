"""
pip install websocket-client
https://pypi.org/project/websocket-client/
"""
import json
import websocket


def on_open(ws):
    """
    on connection to websocket
    send auth message here if needed
    """
    print("BINANCE Websocket connection opened")


def on_close(ws, close_status_code, close_msg):
    """
    on closing connection to websocket
    """
    print("BINANCE Websocket connection closed")


def on_message(ws, message):
    """
    print message
    """
    # print(message)  # message in string format
    json_message = json.loads(message)  # converts message to dict format
    print(json_message)


def on_error(ws, error):
    """
    print error message
    """
    print(error)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        url="wss://stream.binance.com:9443/ws/btcusdt@trade",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()
