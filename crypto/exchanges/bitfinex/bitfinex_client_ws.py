import websocket
import json

data = []


def on_message(ws, message):
    json_message = json.loads(message)  # converts string to dict format

    data.append(json_message)
    print(json_message)  # raw message - string format


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed Bitfinex ws connection")


def on_open(ws):
    print("Opened Bitfinex ws connection")

    channel_data = {
        "event": "subscribe",
        "channel": "book",
        "symbol": "tUSTUSD",
        "prec": "R0",
        "int": 25,
    }

    ws.send(json.dumps(channel_data))


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://api-pub.bitfinex.com/ws/2",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()  # Set dispatcher to automatic reconnection
