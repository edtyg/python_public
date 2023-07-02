"""
SPOT execution program
"""
import logging

import pandas as pd
from logger_client import LoggerClient

from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET
from python.crypto.exchanges.binance.rest.binance_spot import BinanceSpot


def get_account_balances(client):
    """returns account balances

    Args:
        client (_type_): binance spot client
    """
    account_info = client.get_account_infomation()
    logger.info("retrieving account balances")
    logger.info(account_info)

    balances = account_info["balances"]
    balances_df = pd.DataFrame(balances)

    # convert type to float
    balances_df["free"] = balances_df["free"].astype("float")
    balances_df["locked"] = balances_df["locked"].astype("float")

    balances_df = balances_df.loc[balances_df["free"] > 0]
    balances_df.reset_index(inplace=True, drop=True)

    print(balances_df)
    return balances_df


def get_current_open_orders(client, spot_symbol: str):
    """returns current SPOT open orders by symbol

    Args:
        client (_type_): binance spot client
    """
    current_open_orders = client.get_current_open_orders(
        params={
            "symbol": spot_symbol,
        }
    )
    logger.info("retrieving current open orders")
    logger.info(current_open_orders)

    current_open_orders_df = pd.DataFrame(current_open_orders)

    if not current_open_orders_df.empty:
        print(current_open_orders_df)
        logger.info(current_open_orders_df)
        return current_open_orders_df
    else:
        print("no open orders")


def get_spot_trade_records(client, spot_symbol: str):
    """retrieves trade records

    Args:
        client (_type_): binance spot client
    """
    trade_records = client.get_account_trade_list(
        params={
            "symbol": spot_symbol,
            "limit": 500,
        }
    )
    logger.info(f"retrieving {spot_symbol} trade records")
    logger.info(trade_records)

    trade_records_df = pd.DataFrame(trade_records)

    if not trade_records_df.empty:
        print(trade_records_df)
        return trade_records_df
    else:
        print("no trade records")


def place_multiple_orders(
    client,
    symbol: str,
    side: str,
    clips: int,
    total_qty: float,
    client_ref_price: float,
    bps_price_checking: int,
):
    # initialize with true - goes through a few checks
    trading_status = True

    if total_qty > 25:
        trading_status = False
        print(f"total quantity > {total_qty} adjust to a lower amt")
        logging.info(f"total quantity > {total_qty} adjust to a lower amt")

    clip_size = total_qty / clips
    print(f"clip size = {clip_size}")
    logging.info(f"clip size = {clip_size}")

    orderbook_data = client.get_orderbook(params={"symbol": symbol, "limit": 1})
    print(orderbook_data)
    logging.info("getting orderbook_data")
    logging.info(orderbook_data)

    lowest_ask = float(orderbook_data["asks"][0][0])
    highest_bid = float(orderbook_data["bids"][0][0])
    print(f"lowest_ask = {lowest_ask}, highest_bid = {highest_bid}")
    logging.info(f"lowest_ask = {lowest_ask}, highest_bid = {highest_bid}")

    price_levels = 2  # evenly space out price levels

    # if sell - use lower ask as reference
    # if buy - use highest bid as reference
    if side == "SELL":
        price = lowest_ask
        price_levels *= 1  # adding to lowest ask
    elif side == "BUY":
        price = highest_bid
        price_levels *= -1  # subtracting from highest bid

    if trading_status is True:
        for clip in range(clips):
            print(f"clip number {clip+1}")
            logging.info(f"placing order for clip number {clip+1}")

            order_price = price + (price_levels * (clip + 1))
            print("order price = {order_price}")
            price_checking = (abs(order_price - client_ref_price)) / client_ref_price
            print(price_checking)
            logging.info(f"price difference checking = {price_checking}")

            bps_check = bps_price_checking / 10000

            if price_checking > bps_check:
                # will not place order
                print(
                    f"order price {bps_price_checking} bps off quoted client price. Will not place order"
                )
                logging.info(
                    f"order price more than {bps_price_checking} bps off quoted client price. Will not place order"
                )
            elif price_checking <= bps_check:
                # will place order
                spot_order = client.post_new_order(
                    params={
                        "symbol": symbol,
                        "side": side,
                        "type": "LIMIT_MAKER",
                        "quantity": clip_size,
                        "price": order_price,
                    }
                )
                print(spot_order)
                logger.info(spot_order)


if __name__ == "__main__":
    binance_client_spot = BinanceSpot(
        apikey=ED_BINANCE_KEY, apisecret=ED_BINANCE_SECRET
    )

    symbol = "BTCUSDT"
    trading_side = "SELL"
    number_of_clips = 5
    total_qty = 0.0022
    client_ref_price = 29120  # price shown to client
    bps_diff = 20  # if px diff > client_ref_price by x bps -> will not place order

    # pull all current spot balances
    spot_balances = get_account_balances(binance_client_spot)

    # pull current open orders by symbol
    spot_open_orders = get_current_open_orders(binance_client_spot, symbol)

    # pull trade records
    spot_trade_records = get_spot_trade_records(binance_client_spot, symbol)

    # placing multiple maker orders
    place_multiple_orders(
        client=binance_client_spot,
        symbol=symbol,
        side=trading_side,
        clips=number_of_clips,
        total_qty=total_qty,
        client_ref_price=client_ref_price,
        bps_price_checking=bps_diff,
    )

    # # placing order here
    # spot_order = binance_client_spot.post_new_order(
    #     params = {
    #         'symbol':symbol,
    #         'side':'SELL',
    #         'type':'LIMIT_MAKER',
    #         'quantity': 0.0023,
    #         'price': 35000,
    #         'newClientOrderId': 'ed_testing1',
    #         }
    #     )
    # print(spot_order)
    # logger.info(spot_order)
    # spot_order_id = spot_order['orderId']

    # # cancel order here
    # cancel_order = binance_client_spot.delete_cancel_order(
    #     params = {
    #         'symbol':symbol,
    #         'orderId': spot_order_id,
    #         }
    #     )
    # print(cancel_order)
    # logger.info(cancel_order)
