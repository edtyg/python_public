"""
uploading binance data
do not include latest row for binance as data is not finalized
offset last row for each call
"""

import asyncio
import json
import time

import pandas as pd
import websockets

from keys.api_work.databases.postgres import SG_TRADING_3_MARKETDATA_WRITE
from src.projects.postgres_database.connection_client import SqlAlchemyConnector


async def get_binance_tick_data(
    client, table_name: str, connection_params: dict, symbol: str, runtime: int
):
    """
    Pulls binance tick data and uploads to our database.
    Run duration sets it to run for a set duration before closing connection

    https://binance-docs.github.io/apidocs/spot/en/#trade-streams

    Args:
        table_name (str): name of postgresql table to upload to
        connection_params (dict): binance websocket conn params
        symbol (str): trading symbol
        run_duration (int): run duration in minutes
    """
    endpoint = "wss://stream.binance.com:9443/ws"

    conn_start_time = time.time()
    conn_end_time = conn_start_time + 60 * runtime
    print(f"running ws conn for {runtime} minutes")

    connect_params = connection_params["connect"]
    disconnect_params = connection_params["disconnect"]

    while True:
        # outer loop to reconnect if ws is disconnected
        try:
            async with websockets.connect(endpoint) as websocket:
                # send connection params
                print(f"sending connect params {connect_params}")
                await websocket.send(json.dumps(connect_params))

                df_final = pd.DataFrame()
                start_time = time.time()

                while True:
                    try:
                        # exits
                        if time.time() > conn_end_time:
                            print(f"sending disconnect params {disconnect_params}")
                            await websocket.send(json.dumps(disconnect_params))
                            break

                        # receive data
                        response = await websocket.recv()
                        response = json.loads(response)

                        response_columns = [
                            "event",
                            "event_time",
                            "symbol",
                            "trade_id",
                            "price",
                            "qty",
                            "buyer_orderid",
                            "seller_orderid",
                            "trade_time",
                            "is_buyer_mm",
                            "ignore",
                        ]
                        df_resp = pd.DataFrame(response, index=[0])
                        df_resp.columns = response_columns

                        # adjust column types
                        df_resp["symbol"] = df_resp["symbol"].astype("string")
                        df_resp["trade_id"] = df_resp["trade_id"].astype("int64")
                        df_resp["price"] = df_resp["price"].astype("float")
                        df_resp["qty"] = df_resp["qty"].astype("float")

                        df_resp["datetime"] = pd.to_datetime(
                            df_resp["trade_time"], unit="ms"
                        )
                        df_resp = df_resp[
                            [
                                "datetime",
                                "symbol",
                                "trade_id",
                                "price",
                                "qty",
                                "is_buyer_mm",
                            ]
                        ]
                        df_resp.set_index("datetime", inplace=True)
                        df_final = pd.concat([df_final, df_resp])
                        print(df_final)

                        end_time = time.time()
                        time_elapsed = end_time - start_time

                        if time_elapsed > 5:
                            print("5 second interval")
                            # upload here
                            with client.engine.connect() as conn:
                                try:
                                    df_final.to_sql(
                                        table_name,
                                        conn,
                                        if_exists="append",
                                        index=True,
                                    )
                                    print("trade uploaded")
                                except Exception as e:
                                    print(e)
                            start_time = time.time()
                            df_final = pd.DataFrame()

                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")

                    except websockets.ConnectionClosed as e:
                        print(f"Connection closed: {e}")
                        # exit inner loop
                        break

                    except Exception as error:
                        print(error)

            if time.time() > conn_end_time:
                break

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed. Reconnecting...")
            await asyncio.sleep(1)


if __name__ == "__main__":
    client = SqlAlchemyConnector(SG_TRADING_3_MARKETDATA_WRITE)
    client.connect("postgres")

    # table to upload to
    symbol = "btcusdt"
    table_name = "binance_spot_btcusdt_tick_data"
    params = {
        "connect": {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@aggTrade"],
            "id": 1,
        },
        "disconnect": {
            "method": "UNSUBSCRIBE",
            "params": [f"{symbol.lower()}@aggTrade"],
            "id": 312,
        },
    }

    asyncio.get_event_loop().run_until_complete(
        get_binance_tick_data(client, table_name, params, "btcusdt", 0.5)
    )
