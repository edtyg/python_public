"""
MARGIN execution program
"""
import logging
import os
import time

import pandas as pd
from binance_margin import BinanceMargin
from keys import MCA_TRADE_KEY, MCA_TRADE_SECRET, ED_BINANCE_KEY, ED_BINANCE_SECRET

################
### logging ####
full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"
log_file = "client_orders_execution_margin.log"
logging.basicConfig(
    filename=save_path + log_file,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="a",
)
logger = logging.getLogger(__name__)
################


def get_account_balances(client):
    account_info = client.get_isolated_margin_info()
    logger.info("retrieving account balances")
    logger.info(account_info)
    balances = account_info["assets"]

    try:
        balances = balances[0]
        base_asset = balances["baseAsset"]
        quote_asset = balances["quoteAsset"]

        base_asset_df = pd.DataFrame(base_asset, index=[0])
        quote_asset_df = pd.DataFrame(quote_asset, index=[0])

        balances_df = pd.concat([base_asset_df, quote_asset_df])
        balances_df.reset_index(inplace=True, drop=True)

        print(balances_df)
        logger.info(balances_df)
        return balances_df

    except:
        balances_df = pd.DataFrame()
        print(balances_df)
        logger.info(balances_df)
        return balances_df


def get_current_open_orders(client, symbol):
    current_open_orders = client.margin_open_orders(
        params={"symbol": symbol, "isIsolated": "TRUE"}
    )
    logger.info("retrieving current open orders")
    logger.info(current_open_orders)

    current_open_orders_df = pd.DataFrame(current_open_orders)

    if current_open_orders_df.empty == False:
        print(current_open_orders_df)
        logger.info(current_open_orders_df)
        return current_open_orders_df
    else:
        print("no open orders")


def get_margin_trade_records(client, spot_symbol: str):
    """retrieves trade records

    Args:
        client (_type_): binance spot client
    """
    trade_records = client.get_margin_trade_list(
        params={
            "symbol": spot_symbol,
            "isIsolated": "TRUE",
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
                spot_order = client.margin_new_order(
                    params={
                        "symbol": symbol,
                        "side": side,
                        "type": "LIMIT_MAKER",
                        "quantity": clip_size,
                        "price": order_price,
                        "sideEffectType": "MARGIN_BUY",
                        "isIsolated": "TRUE",
                    }
                )
                print(spot_order)
                logger.info(spot_order)


if __name__ == "__main__":
    binance_client_margin = BinanceMargin(
        apikey=ED_BINANCE_KEY, apisecret=ED_BINANCE_SECRET
    )

    symbol = "BTCUSDT"
    trading_side = "BUY"
    number_of_clips = 5
    total_qty = 0.005
    client_ref_price = 29120  # price shown to client
    bps_diff = 20  # if px diff > client_ref_price by x bps -> will not place order

    # pull all current spot balances
    margin_balances = get_account_balances(binance_client_margin)

    # pull current open orders by symbol
    margin_open_orders = get_current_open_orders(binance_client_margin, symbol)

    # pull trade records
    margin_trade_records = get_margin_trade_records(binance_client_margin, symbol)

    # pull interests
    margin_interest = binance_client_margin.get_interest_history(
        params={
            # 'asset':'BTC',
            "isolatedSymbol": "BTCUSDT",
            "size": 100,
        }
    )

    # placing multiple maker orders
    # place_multiple_orders(
    #     client=binance_client_margin,
    #     symbol=symbol,
    #     side=trading_side,
    #     clips=number_of_clips,
    #     total_qty=total_qty,
    #     client_ref_price=client_ref_price,
    #     bps_price_checking=bps_diff,
    # )

    # placing order here
    # margin_order = binance_client_margin.margin_new_order(
    #     params={
    #         "symbol": symbol,
    #         "isIsolated": "TRUE",
    #         "side": "SELL",
    #         "type": "LIMIT_MAKER",
    #         "sideEffectType": "MARGIN_BUY",
    #         "quantity": 0.105,
    #         "price": 2000,
    #         }
    #     )
    # print(margin_order)
    # logger.info(margin_order)
    # margin_order_id = margin_order['orderId']

    # # cancel order here
    # cancel_order = binance_client_margin.margin_cancel_order(
    #     params={
    #         "symbol": symbol,
    #         "isIsolated": "TRUE",
    #         "orderId": margin_order_id,
    #         }
    #     )
    # print(cancel_order)
    # logger.info(cancel_order)
