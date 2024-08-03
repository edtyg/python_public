"""
Binance SPOT Account TWAP algo - Market orders
"""

import datetime as dt
import math
import random
import sys
import time

import pandas as pd

from keys.api_work.crypto_exchanges.binance import BINANCE_MCA_MAIN_TRADE
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot
from src.libraries.configparser.config_setter import ConfigSetter
from src.libraries.logging.logger_client import LoggerClient
from src.libraries.telegram.telegram_trade_execution import Telegram

# from keys.api_personal.crypto_exchanges.binance import BINANCE_TRADE


class SpotTwapAlgoMarket(BinanceSpot, LoggerClient, Telegram):
    """
    Args:
        BinanceSpot (_type_): binance spot client
        LoggerClient (_type_): logging client
        Telegram (_type_): telegram client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        BinanceSpot.__init__(self, apikey, apisecret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        Telegram.__init__(self)

        ### trading params ###
        self.base_ticker = None
        self.quote_ticker = None
        self.binance_symbol = None
        self.direction = None
        self.clip_size_type = None
        self.total_trade_size = None
        self.clip_value_limit = None
        self.total_twap_time_seconds = None
        self.time_interval_seconds = None
        self.client_order_id = None
        self.tg_chatgrp = None

        ### calculated params ###
        self.symbol = None
        self.number_of_clips = None
        self.clip_size = None
        self.cumulative_filled_qty_base = 0
        self.cumulative_filled_qty_quote = 0
        self.decimal_place_ticker = None

        ### checking params ##
        self.ticker_current_price = None
        self.required_balance = None
        self.trading_check_counter = 0

        ### offset ###
        self.randomizer_bounds = 0.2  # within 20% of bounds
        self.time_offset = 0

        self.remaining_qty = None  # either base or quote

    def get_coin_value(self, symbol: str):
        """
        Args:
            symbol: 'BTC', 'ETH' ...

        gets ticker price for symbol against USDT
        """
        stablecoin_list = ["USDT", "TUSD", "USDC"]
        if symbol in stablecoin_list:
            price = 1
        else:
            price = float(
                self.get_symbol_price_ticker({"symbol": f"{symbol}USDT"})["price"]
            )
        return price

    def get_ticker_info(self, ticker: str):
        """
        Args:
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        returns infomation on ticker
        """
        exchange_info = self.get_exchange_information({"symbol": ticker})
        df_exchange_info = pd.DataFrame(exchange_info["symbols"])
        df_symbol_info = df_exchange_info.loc[df_exchange_info["symbol"] == ticker]
        return df_symbol_info

    def get_spot_balance(self, symbol):
        """
        Args:
            symbol: 'BTC', 'ETH', etc...

        returns spot free balance for symbol
        """
        balance = False
        while balance is False:
            try:
                spot_balance = self.post_user_asset()
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
                print(f"sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
        return bal

    def randomizer(
        self,
        count: float,
        lower_bound: float,
        upper_bound: float,
        sum_values: float,
        rounding: float = None,
    ):
        """
        generates a list of random values with preset bounds that sums up to
        a selected value.
        Used for generating clip sizes and sleep timings

        Args:
            count (int): The number of random values to generate.
            lower_bound (float): The minimum value of the range (inclusive).
            upper_bound (float): The maximum value of the range (inclusive).
            sum_values (float): The desired sum of the generated values.
            rounding (float): rounds to specified decimal places
        """
        print(f"generating {count} values with sum = {sum_values}")

        if lower_bound < 0 or upper_bound < 0:
            print("please select non-negative upper and lower bounds")
            return None

        if upper_bound - lower_bound >= lower_bound:
            print("please select smaller bounds or one that's more positive")
            return None

        if (
            count <= 0
            or sum_values < count * lower_bound
            or sum_values > count * upper_bound
        ):
            print("please select different parameters")
            return None

        values = []

        # generate values that are within the bounds
        for _ in range(int(count)):
            value = random.uniform(lower_bound, upper_bound)
            values.append(value)
            sum_values -= value  # calculates the excess or shortfall from target amt

        # offset each element by this amount
        offset = sum_values / count

        for i, j in enumerate(values):
            values[i] += offset
            if rounding:
                values[i] = round(values[i], rounding)

        print(f"values = {values}")
        print(f"count of values = {len(values)}")
        print(f"sum of values = {sum(values)}")
        return values

    def twap_order_checking(self, order_params: dict):
        """
        SPOT TWAP order checking
        can be in terms of base or quote currency
        will do a couple of checks before placing orders

        Args:
            order_params: order parameters
        """

        # counter for checks
        self.trading_check_counter = 0

        ### trading parameters ###
        self.base_ticker = str(order_params["base_ticker"].upper())
        self.quote_ticker = str(order_params["quote_ticker"].upper())
        self.binance_symbol = str(order_params["binance_symbol"].upper())
        self.direction = str(order_params["direction"].upper())
        self.clip_size_type = str(order_params["clip_size_type"].upper())
        self.total_trade_size = float(order_params["total_trade_size"])
        self.clip_value_limit = float(order_params["clip_value_limit"])
        self.total_twap_time_seconds = int(order_params["total_twap_time_seconds"])
        self.time_interval_seconds = int(order_params["time_interval_seconds"])
        self.client_order_id = str(order_params["client_order_id"])
        self.tg_chatgrp = int(order_params["tg_chatgrp"])

        ##########################
        if self.clip_size_type == "BASE":
            self.symbol = self.base_ticker
        elif self.clip_size_type == "QUOTE":
            self.symbol = self.quote_ticker

        print(f"BINANCE {self.binance_symbol} TWAP {self.direction} order")
        print(f"total trade size = {self.total_trade_size} {self.symbol}")
        print(f"order size on based on {self.clip_size_type} currency")
        print("conducting some checks")
        print("\n")

        ##############################
        ### conducting some checks ###
        ##############################

        ### check on number of clips ###
        # choose a time and interval such that clips are integers
        self.number_of_clips = self.total_twap_time_seconds / self.time_interval_seconds
        print(f"number of clips = {self.number_of_clips}")
        print(f"total time taken in seconds = {self.total_twap_time_seconds}")
        print(f"total time taken in hours = {self.total_twap_time_seconds/3600}")
        print(f"clip intervals in seconds = {self.time_interval_seconds}")

        if int(self.number_of_clips) != self.number_of_clips:
            print("twap time and intervals not suitable")
            print("please choose a different twap time and interval")
            self.trading_check_counter += 1
            return None

        ### checking on binance_symbol ###
        # checking on ticker step size and round clip to that decimal place
        if self.binance_symbol != self.base_ticker + self.quote_ticker:
            print("please check on base and quote ticker")
            print("does not match binance symbol")
            self.trading_check_counter += 1
            return None

        df_symbol_info = self.get_ticker_info(self.binance_symbol)
        if not df_symbol_info.empty:
            filters = df_symbol_info["filters"].values[0]
            lot_size = filters[1]
            step_size = float(lot_size["stepSize"])
            self.decimal_place_ticker = int(math.log(1 / step_size, 10))
            self.clip_size = round(
                self.total_trade_size / self.number_of_clips, self.decimal_place_ticker
            )
            print(f"clip size = {self.clip_size} {self.symbol}")
        else:
            print("please check on binance symbol - it does not exist")
            self.trading_check_counter += 1
            return None

        ### check if clip value is greater than pre-set clip limit ###
        clip_value = self.get_coin_value(self.symbol) * self.clip_size
        print(f"clip value = {clip_value}")
        if clip_value > self.clip_value_limit:
            print(f"clip value exceeds limit of {self.clip_value_limit}")
            print("please adjust trade size or clip intervals")
            self.trading_check_counter += 1
            return None

        ### check if min trade size is satisfied ###
        if clip_value < 5:
            print("clip value less than binance min trade size of 5 USD")
            self.trading_check_counter += 1
            return None

        ### check if we have sufficient balance for orders ###
        # base asset
        base_asset_balance = self.get_spot_balance(self.base_ticker)
        print(f"current {self.base_ticker} balance = {base_asset_balance}")
        base_asset_balance_val = (
            self.get_coin_value(self.base_ticker) * base_asset_balance
        )
        print(f"current {self.base_ticker} valuation = {base_asset_balance_val}")

        # quote asset
        quote_asset_balance = self.get_spot_balance(self.quote_ticker)
        print(f"current {self.quote_ticker} balance = {quote_asset_balance}")
        quote_asset_balance_val = (
            self.get_coin_value(self.quote_ticker) * quote_asset_balance
        )
        print(f"current {self.quote_ticker} valuation = {quote_asset_balance_val}")
        print("\n")

        # get current ticker price
        self.ticker_current_price = float(
            self.get_symbol_price_ticker(params={"symbol": self.binance_symbol})[
                "price"
            ]
        )

        if self.direction == "BUY" and self.clip_size_type == "BASE":
            # check if sufficient quote asset balance
            self.required_balance = self.ticker_current_price * self.total_trade_size
            if quote_asset_balance < self.required_balance:
                print("insufficient quote balance")
                print(f"current quote balance = {quote_asset_balance}")
                print(f"required quote balance = {self.required_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "BUY" and self.clip_size_type == "QUOTE":
            self.required_balance = self.total_trade_size
            if quote_asset_balance < self.required_balance:
                print("insufficient quote balance")
                print(f"current quote balance = {quote_asset_balance}")
                print(f"required quote balance = {self.required_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "BASE":
            self.required_balance = self.total_trade_size
            if base_asset_balance < self.required_balance:
                print("insufficient base balance")
                print(f"required base balance = {self.required_balance}")
                print(f"current base balance = {base_asset_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "QUOTE":
            if base_asset_balance_val < self.total_trade_size:
                print("insufficient base balance")
                print(f"current base balance = {base_asset_balance}")
                print(f"current base balance valuation = {base_asset_balance_val}")
                print(f"required base balance valuation = {self.total_trade_size}")
                self.trading_check_counter += 1
                return None

        print(f"twap time = {self.total_twap_time_seconds} seconds")
        print(f"clip_interval = {self.time_interval_seconds} seconds")
        print("\n")

        if self.trading_check_counter == 0:
            print("all checks passed")
            print("\n")

    def place_twap_order(self, order_params: dict):
        """
        placing order - does a check first
        """
        self.twap_order_checking(order_params)

        if self.trading_check_counter == 0:
            # setting order parameters here
            placing_order_params = {
                "symbol": self.binance_symbol,
                "side": self.direction,
                "type": "MARKET",
                "newClientOrderId": self.client_order_id,
            }

            # placing order in clips
            time_interval_seconds = self.time_interval_seconds
            number_of_clips = self.total_twap_time_seconds / self.time_interval_seconds

            ### setting up randomizer ###
            # randomizing clips
            randomized_clip_sizes = self.randomizer(
                number_of_clips,
                self.clip_size * (1 - self.randomizer_bounds),
                self.clip_size * (1 + self.randomizer_bounds),
                self.total_trade_size,
                self.decimal_place_ticker,
            )
            # randomizing sleep time
            randomized_sleep_time = self.randomizer(
                number_of_clips,
                time_interval_seconds * (1 - self.randomizer_bounds),
                time_interval_seconds * (1 + self.randomizer_bounds),
                self.total_twap_time_seconds,
            )

            # set remaining qty
            self.remaining_qty = self.total_trade_size

            # algo start message
            try:
                self.send_message(
                    self.tg_chatgrp,
                    f"""
                    {self.fire_emoji*3}\
                    \nStarting TWAP MARKET {self.direction} order for {self.binance_symbol}\
                    \nnumber of clips = {self.number_of_clips}\
                    \ntotal size = {self.total_trade_size} {self.symbol}\
                    \n{self.fire_emoji*3}\
                    """,
                )
            except Exception as ex:
                self.logger.exception(ex)
                self.logger.warning("telegram exception: continuing with execution")

            i = 0
            tg_counter = 0
            while i < int(number_of_clips):
                try:
                    clip_size_randomized = randomized_clip_sizes[i]
                    sleep_time_randomized = randomized_sleep_time[i]

                    start_time = time.time()  # start time

                    # either quantity or quoteOrderQty
                    clip_size_type = self.clip_size_type

                    # sets minumum of remaining qty or randomized size rounded down
                    # should fix last clip issue
                    rounded = (
                        math.floor(self.remaining_qty * 10**self.decimal_place_ticker)
                        / 10**self.decimal_place_ticker
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)

                    if clip_size_type == "BASE":
                        placing_order_params["quantity"] = clip_size_randomized
                    elif clip_size_type == "QUOTE":
                        placing_order_params["quoteOrderQty"] = clip_size_randomized

                    # placing order here
                    order = self.post_order(placing_order_params)
                    print(order)

                    if order["status"] != "FILLED":
                        time.sleep(0.1)
                        continue

                    self.logger.info(order)
                    clip_symbol = order["symbol"]
                    clip_orderid = order["orderId"]
                    clip_transact_time = order["transactTime"]
                    clip_direction = order["side"]
                    clip_fill_details = order["fills"]
                    clip_fill_qty_quote = float(order["cummulativeQuoteQty"])
                    self.cumulative_filled_qty_quote += clip_fill_qty_quote

                    clip_filled_qty_base = 0
                    for f in clip_fill_details:
                        clip_filled_qty_base += float(f["qty"])
                    self.cumulative_filled_qty_base += clip_filled_qty_base

                    if clip_size_type == "BASE":
                        self.remaining_qty -= clip_filled_qty_base
                    elif clip_size_type == "QUOTE":
                        self.remaining_qty -= clip_fill_qty_quote

                    # sending tg message
                    if tg_counter % 1 == 0:
                        self.send_message(
                            self.tg_chatgrp,
                            f"""
                            clip {i+1} of {int(number_of_clips)}:\
                            \nplatform = Binance\
                            \nsymbol = {clip_symbol}\
                            \norderId = {clip_orderid}\
                            \ntime = {clip_transact_time}\
                            \nside = {clip_direction}\
                            \nqty_filled_base = {clip_filled_qty_base}\
                            \nqty_filled_quote = {clip_fill_qty_quote}\
                            \ncumulative_qty_base = {self.cumulative_filled_qty_base}\
                            \ncumulative_qty_quote = {self.cumulative_filled_qty_quote}\
                            """,
                        )
                    print(f"clip {i+1} of {int(number_of_clips)} done")

                    end_time = time.time()  # end time
                    self.time_offset += end_time - start_time
                    time_sleep_offset = max(0, sleep_time_randomized - self.time_offset)

                    print(f"sleeping for {time_sleep_offset} seconds")
                    i += 1
                    tg_counter += 1
                    self.time_offset = 0  # reset offset time
                    time.sleep(time_sleep_offset)

                except Exception as error:
                    print(f"placing order error: {error}")
                    self.logger.exception(error)

                    # sending tg message
                    try:
                        self.send_message_error(
                            self.tg_chatgrp,
                            f"{self.alarm_emoji} clip {i+1} error, retrying again {self.alarm_emoji}",
                        )
                    except Exception as ex:
                        self.logger.exception(ex)
                        self.logger.warning(
                            "telegram exception: continuing with execution"
                        )

                    sleep_time = 0.2
                    time.sleep(sleep_time)
                    print(f"slept for {sleep_time} seconds")

            # send message on completion
            self.send_message(
                self.tg_chatgrp,
                f"""
                {self.fire_emoji*3}\
                \norder completed please check\
                \n{self.fire_emoji*3}\
                """,
            )


if __name__ == "__main__":
    config_path = sys.argv[1]
    log_path = sys.argv[2] + dt.datetime.now().strftime("%Y-%m-%d") + "-"
    mode = sys.argv[3]
    trading_params = sys.argv[4]

    # config_path = "C:/Users/EdgarTan/Documents/Github/python/config/trade_execution_algos/binance/binance_spot_twap_market.ini"
    # log_path = f"C:/Users/EdgarTan/Documents/Github/python/logs/trade_execution_algos/binance/{dt.datetime.now().strftime('%Y-%m-%d')}-"
    # mode = "check"
    # trading_params = "btcusdt-params"

    cfg = ConfigSetter(config_path)
    MARKET_PARAMS = cfg.get_section_data(trading_params)

    # for saving logs
    FILENAME = MARKET_PARAMS["client_order_id"] + ".log"  # setting log file as orderid

    # initializing
    client = SpotTwapAlgoMarket(
        apikey=BINANCE_MCA_MAIN_TRADE["api_key"],
        apisecret=BINANCE_MCA_MAIN_TRADE["api_secret"],
        file_path=log_path,
        file_name=FILENAME,
        save_mode="a",
    )

    if mode.lower() == "check":
        client.twap_order_checking(MARKET_PARAMS)
    elif mode.lower() == "trade":
        client.place_twap_order(MARKET_PARAMS)
