"""
Binance Spread trading algo - Spot vs Coinm futures only

checks:
spot ticker
futures ticker
sufficient spot balances
"""

import math
import os
import sys
import time

import pandas as pd

from src.crypto.exchanges.binance.rest.binance_coinm import BinanceCoinm
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot
from src.crypto.execution_algo.binance.binance_spread_trading.config_spreads import (
    SPREAD_PARAMS,
    TRADING_ACCOUNT,
)
from src.libraries.logging.logger_client import LoggerClient
from src.libraries.telegram.telegram_trade_execution import Telegram


class SpreadAlgo(BinanceSpot, BinanceCoinm, LoggerClient, Telegram):
    """
    Args:
        BinanceSpot (_type_): binance spot client
        BinanceCoinm (_type_): binance coinm client
        LoggerClient (_type_): logging client
        Telegram (_type_): telegram client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        BinanceSpot.__init__(self, apikey, apisecret)
        BinanceCoinm.__init__(self, apikey, apisecret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        Telegram.__init__(self)

        ### trading params ###
        self.spot_base_ticker = None
        self.spot_quote_ticker = None
        self.spot_ticker = None

        self.futures_ticker = None
        self.spread_direction = None
        self.total_trade_size = None
        self.clip_size_type = None
        self.contract_clip_size = None  # preset contract clip qty
        self.time_interval_seconds = None
        self.client_order_id = None
        self.tg_chatgrp = None

        ### calculated params ###
        self.estimated_time = None
        self.spot_price_decimals = None  # spot price max decimal places
        self.spot_amt_decimals = None  # spot amt max decimal places
        self.contract_value = None  # clip size * contract size

        self.futures_cumulative_filled_contracts = 0
        self.futures_cumulative_filled_base_ccy = 0
        self.spot_cumulative_filled_base_ccy = 0
        self.spot_cumulative_filled_quote_ccy = 0

        ### others ###
        self.trading_check_counter = 0
        self.spot_ticker_price = None
        self.required_balance = None
        self.contract_size = None  # 100 for btc, 10 for eth
        self.remaining_qty = None
        self.spot_direction = None
        self.futures_direction = None

    def get_coin_value(self, symbol: str):
        """
        Args:
            symbol: 'BTC' or 'ETH' etc...

        returns symbol valuation in USDT terms, or 1 if stablecoin
        """
        stablecoin_list = ["USDT", "USDC"]
        if symbol in stablecoin_list:
            price = 1
        else:
            price = float(
                self.get_symbol_price_ticker({"symbol": f"{symbol}USDT"})["price"]
            )
        return price

    def get_spot_balance(self, symbol):
        """
        returns spot free balance for symbol

        Args:
            symbol: 'BTC', 'ETH', etc...

        """
        balance = False
        while balance is False:
            try:
                spot_balance = self.post_spot_user_asset()
                df_assets = pd.DataFrame(spot_balance)
                balance = df_assets.loc[df_assets["asset"] == symbol, "free"]

                if not balance.empty:
                    bal = float(balance.values[0])
                else:
                    bal = 0
                balance = True
            except Exception as error:
                print(f"pulling balance error: {error}")
                print("trying again")
                sleep_time = 1
                time.sleep(sleep_time)
                print(f"sleeping for {sleep_time} seconds")
        return bal

    def get_coinm_balance(self, symbol):
        """
        returns coinm account balances

        Args:
            symbol: 'BTC', 'ETH', etc...

        """
        balance = False
        while balance is False:
            try:
                coinm_balance = self.get_coinm_account_balance()
                df_coinm = pd.DataFrame(coinm_balance)
                balance = df_coinm.loc[df_coinm["asset"] == symbol, "balance"]

                if not balance.empty:
                    bal = float(balance.values[0])
                else:
                    bal = 0
                balance = True

            except Exception as error:
                print(f"pulling balance error: {error}. trying again")
                sleep_time = 1
                time.sleep(sleep_time)
                print(f"sleeping for {sleep_time} seconds")
        return bal

    def spread_order_checking(self, order_params: dict):
        """
        does some checks first before placing orders
        """

        # counter for checks
        self.trading_check_counter = 0

        ### trading parameters ###
        self.spot_base_ticker = order_params["spot_base_ticker"].upper()
        self.spot_quote_ticker = order_params["spot_quote_ticker"].upper()
        self.spot_ticker = order_params["spot_ticker"].upper()
        self.futures_ticker = order_params["futures_ticker"].upper()
        self.spread_direction = order_params["spread_direction"].upper()
        self.total_trade_size = float(order_params["total_trade_size"])
        self.clip_size_type = order_params["clip_size_type"].upper()
        self.contract_clip_size = order_params["contract_clip_size"]
        self.time_interval_seconds = order_params["time_interval_seconds"]
        self.client_order_id = order_params["client_order_id"]
        self.tg_chatgrp = order_params["tg_chatgrp"]

        ##########################

        if self.clip_size_type == "BASE":
            self.symbol = self.spot_base_ticker
        elif self.clip_size_type == "QUOTE":
            self.symbol = self.spot_quote_ticker

        print(f"Binance Spread Algo")
        if self.spread_direction == "SELL":
            self.spot_direction = "BUY"
            self.futures_direction = "SELL"
            print(
                f"{self.futures_direction} {self.futures_ticker}, {self.spot_direction} {self.spot_ticker}"
            )

        elif self.spread_direction == "BUY":
            self.spot_direction = "SELL"
            self.futures_direction = "BUY"
            print(
                f"{self.futures_direction} {self.futures_ticker}, {self.spot_direction} {self.spot_ticker}"
            )

        print(f"total trade size = {self.total_trade_size} {self.symbol}")
        print(f"order size on based on {self.clip_size_type} currency")
        print("conducting some checks")
        print("\n")

        ##############################
        ### conducting some checks ###
        ##############################

        ### checking on binance_symbol ###
        if self.spot_ticker != self.spot_base_ticker + self.spot_quote_ticker:
            print("please check on base and quote ticker")
            print("does not match binance symbol")
            self.trading_check_counter += 1
            return None

        # check if spot ticker exists + get tick size and step size
        try:
            spot_info = self.get_spot_exchange_information({"symbol": self.spot_ticker})
            spot_tick_size = spot_info["symbols"][0]["filters"][0]["tickSize"]
            spot_step_size = spot_info["symbols"][0]["filters"][1]["stepSize"]
            self.spot_price_decimals = int(math.log(1 / float(spot_tick_size), 10))
            self.spot_amt_decimals = int(math.log(1 / float(spot_step_size), 10))
            try:
                if spot_info["msg"] == "Invalid symbol.":
                    self.trading_check_counter += 1
                    print("spot ticker does not exist")
                    return None
            except KeyError:
                pass
        except Exception as e:
            print(e)
        else:
            print(f"spot ticker {self.spot_ticker} is valid")

        # check if futures ticker exist - saving contract size in USD
        try:
            coinm = self.get_coinm_exchange_info()
            df_coinm = pd.DataFrame(coinm["symbols"])
            try:
                coinm_data = df_coinm.loc[df_coinm["symbol"] == self.futures_ticker]
                self.contract_size = float(coinm_data["contractSize"].values[0])
                print(f"{self.futures_ticker} contract size = {self.contract_size}")
                self.contract_value = self.contract_clip_size * self.contract_size
                if coinm_data.empty:
                    self.trading_check_counter += 1
                    print("futures ticker does not exist")
                    return None
            except KeyError:
                pass
        except Exception as e:
            print(e)
        else:
            print(f"futures ticker {self.futures_ticker} is valid")

        ### check if we have sufficient balance for orders ###
        base_asset_balance = self.get_spot_balance(self.spot_base_ticker)
        print(f"current {self.spot_base_ticker} balance = {base_asset_balance}")
        base_val = self.get_coin_value(self.spot_base_ticker) * base_asset_balance
        print(f"current {self.spot_base_ticker} valuation = {base_val}")

        quote_asset_balance = self.get_spot_balance(self.spot_quote_ticker)
        print(f"current {self.spot_quote_ticker} balance = {quote_asset_balance}")
        quote_val = self.get_coin_value(self.spot_quote_ticker) * quote_asset_balance
        print(f"current {self.spot_quote_ticker} valuation = {quote_val}")
        print("\n")

        self.spot_ticker_price = float(
            self.get_symbol_price_ticker(params={"symbol": self.spot_ticker})["price"]
        )

        if self.spread_direction == "SELL":
            # Sell futures, Buy Spot
            if self.clip_size_type == "BASE":
                # Buy spot in base currency terms -> check if sufficient quote ccy
                self.required_balance = self.spot_ticker_price * self.total_trade_size
                if quote_asset_balance < self.required_balance:
                    print("insufficient quote balance")
                    print(f"current quote balance = {quote_asset_balance}")
                    print(f"required quote balance = {self.required_balance}")
                    self.trading_check_counter += 1
                    return None

            elif self.clip_size_type == "QUOTE":
                # Buy spot in quote currency terms -> check if sufficient quote ccy
                self.required_balance = self.total_trade_size
                if quote_asset_balance < self.required_balance:
                    print("insufficient quote balance")
                    print(f"current quote balance = {quote_asset_balance}")
                    print(f"required quote balance = {self.required_balance}")
                    self.trading_check_counter += 1
                    return None

        elif self.spread_direction == "BUY":
            # Buy futures, Sell Spot
            if self.clip_size_type == "BASE":
                # Sell spot in base currency terms -> check if sufficient base
                self.required_balance = self.total_trade_size
                if base_asset_balance < self.required_balance:
                    print("insufficient base balance")
                    print(f"current base balance = {base_asset_balance}")
                    print(f"required base balance = {self.required_balance}")
                    self.trading_check_counter += 1
                    return None

            elif self.clip_size_type == "QUOTE":
                # Sell spot in quote currency terms -> check if sufficient base
                self.required_balance = self.total_trade_size / self.spot_ticker_price
                if base_asset_balance < self.required_balance:
                    print("insufficient base balance")
                    print(f"current base balance = {base_asset_balance}")
                    print(f"required base balance = {self.required_balance}")
                    self.trading_check_counter += 1
                    return None

        if self.trading_check_counter == 0:
            print("all checks passed")
            print("\n")

    def place_spread_order(self, order_params: dict):
        """
        placing order - does a check first
        """

        ### checks here ###
        self.spread_order_checking(order_params)
        if self.trading_check_counter != 0:
            print("checks failed")
            return

        # set remaining quantity and time
        self.remaining_qty = self.total_trade_size

        # algo start message
        try:
            self.send_message(
                self.tg_chatgrp,
                f"""
                {self.fire_emoji*3}\
                \nStarting Spread order\
                \n{self.futures_direction} {self.futures_ticker}, {self.spot_direction} {self.spot_ticker}\
                \ntotal size = {self.total_trade_size} {self.symbol}\
                \n{self.fire_emoji*3}\
                """,
            )
        except Exception as e:
            self.logger.exception(e)
            self.logger.warning("telegram exception: continuing with execution")

        ###########################
        ### Placing orders here ###
        ###########################

        clip_counter = 0
        order_status = True
        while order_status is True:
            try:
                if self.clip_size_type == "BASE":
                    # calculates remaining qty valuation
                    self.spot_ticker_price = float(
                        self.get_symbol_price_ticker(
                            params={"symbol": self.spot_ticker}
                        )["price"]
                    )
                    remaining_valuation = self.spot_ticker_price * self.remaining_qty
                elif self.clip_size_type == "QUOTE":
                    # calculates remaining quote qty valuation -> take as 1:1 with USD
                    remaining_valuation = self.remaining_qty
                print(f"remaining valuation = {remaining_valuation}")

                if self.contract_value > remaining_valuation:
                    # place last order
                    print("placing last clip")
                    remaining_valuation = (
                        int(math.floor(remaining_valuation / self.contract_size))
                        * self.contract_size
                    )
                    self.contract_clip_size = remaining_valuation / self.contract_value
                    order_status = False  # exits order loop
                    print(f"final clip size = {self.contract_clip_size}")
                    if self.contract_clip_size == 0:
                        print("final clip = 0")
                        order_status = False
                        continue

                ### Futures order here ###
                futures_order_params = {
                    "symbol": self.futures_ticker,
                    "side": self.futures_direction,
                    "type": "MARKET",
                    "newClientOrderId": self.client_order_id,
                    "quantity": self.contract_clip_size,
                }

                futures_order_status = False
                while futures_order_status is False:
                    try:
                        # place futures orders
                        print("placing futures order")
                        fut_order = self.post_coinm_order(futures_order_params)
                        self.logger.info(fut_order)
                        futures_order_id = fut_order["orderId"]

                        # retrieve order details
                        print("retrieving futures order details")
                        fut_details = self.get_coinm_order(
                            {"symbol": self.futures_ticker, "orderId": futures_order_id}
                        )
                        if fut_details["status"] == "FILLED":
                            self.logger.info(fut_details)
                            futures_order_status = True
                            fut_orderid = fut_details["orderId"]
                            fut_symbol = fut_details["symbol"]
                            fut_avg_px = fut_details["avgPrice"]
                            fut_qty = fut_details["executedQty"]
                            fut_cum_base = fut_details["cumBase"]
                            fut_side = fut_details["side"]
                            fut_time = fut_details["time"]
                            self.futures_cumulative_filled_contracts += float(fut_qty)
                            self.futures_cumulative_filled_base_ccy += float(
                                fut_cum_base
                            )

                            print("sending telegram message")
                            self.send_message(
                                self.tg_chatgrp,
                                f"""
                                clip {clip_counter}:\
                                \nplatform = Binance\
                                \ntype = Futures Leg\
                                \nsymbol = {fut_symbol}\
                                \norderId = {fut_orderid}\
                                \ntime = {fut_time}\
                                \nside = {fut_side}\
                                \nqty_filled_contracts = {fut_qty}\
                                \nqty_filled_base_ccy = {fut_cum_base}\
                                \naverage_px = {fut_avg_px}\
                                \ncumulative_qty_contracts = {self.futures_cumulative_filled_contracts}\
                                \ncumulative_qty_base_ccy = {self.futures_cumulative_filled_base_ccy}\
                                """,
                            )
                    except Exception as e:
                        print(e)

                ### Spot Order here ###
                spot_order_params = {
                    "symbol": self.spot_ticker,
                    "side": self.spot_direction,
                    "type": "MARKET",
                    "newClientOrderId": self.client_order_id,
                    "quantity": round(float(fut_cum_base), self.spot_amt_decimals),
                }

                spot_order_status = False
                while spot_order_status is False:
                    try:
                        # place orders
                        print("placing spot order")
                        spot_order = self.post_spot_order(spot_order_params)

                        if spot_order["status"] == "FILLED":
                            self.logger.info(spot_order)
                            spot_order_status = True

                            spot_orderid = spot_order["orderId"]
                            spot_symbol = spot_order["symbol"]
                            spot_base_qty = spot_order["executedQty"]
                            spot_cum_quote_qty = spot_order["cummulativeQuoteQty"]
                            spot_side = spot_order["side"]
                            spot_time = spot_order["transactTime"]
                            spot_avg_px = float(spot_cum_quote_qty) / float(
                                spot_base_qty
                            )
                            spot_fills = spot_order["fills"]
                            self.spot_cumulative_filled_base_ccy += float(spot_base_qty)
                            self.spot_cumulative_filled_quote_ccy += float(
                                spot_cum_quote_qty
                            )

                            print("sending telegram message")
                            self.send_message(
                                self.tg_chatgrp,
                                f"""
                                clip {clip_counter}:\
                                \nplatform = Binance\
                                \ntype = Spot Leg\
                                \nsymbol = {spot_symbol}\
                                \norderId = {spot_orderid}\
                                \ntime = {spot_time}\
                                \nside = {spot_side}\
                                \nqty_filled_base_ccy = {spot_base_qty}\
                                \nqty_filled_base_ccy = {spot_cum_quote_qty}\
                                \naverage_px = {spot_avg_px}\
                                \ncumulative_qty_base_ccy = {self.spot_cumulative_filled_base_ccy}\
                                \ncumulative_qty_quote_ccy = {self.spot_cumulative_filled_quote_ccy}\
                                """,
                            )

                            if self.clip_size_type == "BASE":
                                self.remaining_qty -= float(spot_base_qty)
                            elif self.clip_size_type == "QUOTE":
                                self.remaining_qty -= float(spot_cum_quote_qty)

                            # transfers spot tokens over to coinm account
                            # need to account if fees not paid in bnb
                            df_coin_fills = pd.DataFrame(spot_fills)
                            df_fees = df_coin_fills.loc[
                                df_coin_fills["commissionAsset"]
                                == self.spot_base_ticker
                            ]
                            if not df_fees.empty:
                                # if fees paid
                                fees = df_fees["commission"].astype("float").sum()
                                transfer_amt = spot_base_qty - fees
                            else:
                                transfer_amt = spot_base_qty

                            print("transferring spot tokens to futures account")
                            transfer = self.post_user_universal_transfer(
                                {
                                    "type": "MAIN_CMFUTURE",
                                    "asset": self.spot_base_ticker,
                                    "amount": transfer_amt,
                                }
                            )
                            self.logger.info(transfer)
                            print(f"remaining qty = {self.remaining_qty}")

                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)

            clip_counter += 1

            print("sleeping")
            time.sleep(5)

        # send message on completion
        self.send_message(
            self.tg_chatgrp,
            f"""
            {self.fire_emoji*3}\
            \nSpread order completed please check\
            \n{self.fire_emoji*3}\
            """,
        )


if __name__ == "__main__":
    # mode = sys.argv[1]

    mode = "trade"

    # for saving logs
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = SPREAD_PARAMS["client_order_id"] + ".log"  # setting log file as orderid
    # print(FILENAME)

    # initializing
    client = SpreadAlgo(
        apikey=TRADING_ACCOUNT["api_key"],
        apisecret=TRADING_ACCOUNT["api_secret"],
        file_path=save_path,
        file_name=FILENAME,
        save_mode="a",
    )

    if mode.lower() == "check":
        client.spread_order_checking(SPREAD_PARAMS)
    elif mode.lower() == "trade":
        client.place_spread_order(SPREAD_PARAMS)
