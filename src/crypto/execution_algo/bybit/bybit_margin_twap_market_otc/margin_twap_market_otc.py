"""
BYBIT Margin TWAP algo
"""

import ast
import datetime as dt
import math
import random
import sys
import time

import pandas as pd

from keys.api_work.crypto_exchanges.bybit import BYBIT_MCA_LTP1_TRADE
from src.crypto.exchanges.bybit.rest.bybit_client import Bybit
from src.libraries.configparser.config_setter import ConfigSetter
from src.libraries.logging.logger_client import LoggerClient
from src.libraries.telegram.telegram_trade_execution import Telegram


class MarginTwapAlgoMarketOTC(Bybit, LoggerClient, Telegram):
    """
    Args:
        Okx (_type_): Okx spot client
        LoggerClient (_type_): logging client
        Telegram (_type_): telegram client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        Bybit.__init__(self, apikey, apisecret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        Telegram.__init__(self)

        ### trading params ###
        self.base_ticker = None
        self.quote_ticker = None
        self.bybit_symbol = None
        self.direction = None
        self.clip_size_type = None
        self.clip_value_limit = None
        self.total_trade_size = None
        self.total_twap_time_seconds = None
        self.time_interval_seconds = None
        self.proportions = None
        self.client_order_id = None
        self.leverage_ratio = None
        self.tg_chatgrp = None

        ### calculated params ###
        self.symbol = None
        self.number_of_clips = None
        self.clip_size = None
        self.cumulative_filled_qty_base = 0
        self.cumulative_filled_qty_quote = 0
        self.decimal_place_ticker = None

        self.proportioned_clip_sizes = None
        self.randomized_sleep_time = None

        ### checking params ##
        self.ticker_current_price = None
        self.required_balance = None
        self.trading_check_counter = 0

        ### offset ###
        self.randomizer_bounds = 0.2  # within 20% of bounds
        self.time_offset = 0

        self.remaining_qty = None  # either base or quote

    def get_coin_value(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH' ...

        gets ticker price for symbol against USDT

        Returns:
            float: 100.00
        """
        stablecoin_list = ["USDT", "TUSD", "USDC"]
        if symbol in stablecoin_list:
            ref_price = 1
        else:
            try:
                price = self.get_tickers(
                    {
                        "category": "spot",
                        "symbol": f"{symbol.upper()}USDT",
                    }
                )
                ref_price = price["result"]["list"][0]["lastPrice"]
            except Exception as error:
                print(error)
        return float(ref_price)

    def get_ticker_info(self, ticker: str):
        """
        returns infomation on ticker

        Args:
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        Returns:
            pd.DataFrame

        basePrecision   quotePrecision  minOrderQty     maxOrderQty     minOrderAmt maxOrderAmt
        0.00001         0.0000001       0.00062         1229.2336343    1           2000000
        """
        exchange_info = self.get_instruments_info(
            {
                "category": "spot",
                "symbol": ticker.upper(),
            }
        )
        df_exchange_info = pd.DataFrame(
            exchange_info["result"]["list"][0]["lotSizeFilter"], index=[0]
        )
        return df_exchange_info

    def get_spot_balance(self, symbol):
        """
        returns spot free balance for symbol

        Args:
            symbol: 'BTC', 'ETH', etc...

        Returns:
            float -> 100.00
        """
        balance = False
        while balance is False:
            try:
                spot_balance = self.get_all_coins_balance({"accountType": "UNIFIED"})
                df_assets = pd.DataFrame(spot_balance["result"]["balance"])

                if df_assets.empty:
                    # base ccy and quote ccy both 0
                    bal = 0
                    balance = True
                else:
                    # have either base ccy or quote ccy balance
                    # one of which might be 0
                    balance = df_assets.loc[
                        df_assets["coin"] == symbol.upper(), "walletBalance"
                    ]

                    if balance.size > 0:
                        bal = float(balance.values[0])
                    else:
                        bal = 0

            except Exception as error:
                print(f"pulling balance error: {error}")
                print("trying again")
                sleep_time = 1
                time.sleep(sleep_time)
                print(f"sleeping for {sleep_time} seconds")
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

        if upper_bound - lower_bound >= lower_bound - 0:
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

    def generate_clip_sizes(
        self,
        clip_count: int,
        total_sum: float,
        proportions: list,
        rounding: int = None,
    ):
        """
        Generates clip sizes in descending order for OTC trade executions
        by dividing the total sum among clips according to preset proportions.

        Args:
            clip_count (int): The number of clip sizes to generate.
            total_sum (float): The desired total sum of the generated clip sizes.
            proportions (list): List of proportions.
            rounding (int): Number of decimal places to round to (optional).

        Returns:
            list: List of generated clip sizes.
        """
        print(f"Generating {clip_count} clip sizes with total sum = {total_sum}")

        # Check if proportions are acceptable
        if any(p <= 0 or not isinstance(p, float) for p in proportions):
            print("Proportions can only be non-zero positive float values.")
            return

        if sum(proportions) != 1:
            print("Sum of proportions has to be 1.")
            return

        if clip_count < len(proportions):
            print(f"Clip count has to be at least >= {len(proportions)}")
            return

        if clip_count % len(proportions) != 0:
            print("select different clip counts and proportions")
            return

        # Calculate clips per proportion and remaining clips
        proportioned_values = [p * total_sum for p in proportions]

        clip_sizes = []
        clip_proportion_length = clip_count // len(proportions)
        for p in proportioned_values:
            clip_sizes += int(clip_proportion_length) * [
                round(p / clip_proportion_length, rounding)
            ]

        print(clip_sizes)
        return clip_sizes

    def get_order_fills(self, order_id, instrument_id: str):
        """
        get fills by orderid
        need to sleep awhile before we retrieve order
        can have multiple fills per order
        """
        trade_fills = False
        while trade_fills is False:
            try:
                trade_record = self.get_trade_history(
                    {
                        "category": "spot",
                        "symbol": instrument_id,
                        "orderId": order_id,
                    }
                )
                if trade_record["result"]["list"]:
                    # only logs if not empty
                    self.logger.info(trade_record)
                    print(trade_record)
                    fills = trade_record["result"]["list"]
                    df_fills = pd.DataFrame(fills)
                    base_fill_qty = df_fills["execQty"].astype("float").sum()
                    quote_fill_qty = df_fills["execValue"].astype("float").sum()
                    trade_fills = True
                    print("retrieving fills successful")
                else:
                    sleep_time = 0.2
                    print(f"No records Yet. Retrying in {sleep_time} seconds")
                    time.sleep(sleep_time)
            except Exception as error:
                print(error)
                sleep_time = 0.2
                print(f"retrieving fills failed. Retrying in {sleep_time} seconds")
                time.sleep(sleep_time)
        return [base_fill_qty, quote_fill_qty, df_fills]

    def twap_order_checking(self, order_params: dict):
        """SPOT TWAP order checking
        can be in terms of base or quote currency
        will do a couple of checks before placing orders

        Args:
            order_params: order parameters
        """

        # counter for checks
        self.trading_check_counter = 0

        ### trading parameters from config file ###
        self.base_ticker = str(order_params["base_ticker"].upper())
        self.quote_ticker = str(order_params["quote_ticker"].upper())
        self.bybit_symbol = str(order_params["bybit_symbol"].upper())
        self.direction = str(order_params["direction"].upper())
        self.clip_size_type = str(order_params["clip_size_type"].upper())
        self.total_trade_size = float(order_params["total_trade_size"])
        self.clip_value_limit = float(order_params["clip_value_limit"])
        self.total_twap_time_seconds = int(order_params["total_twap_time_seconds"])
        self.time_interval_seconds = int(order_params["time_interval_seconds"])
        self.proportions = ast.literal_eval(order_params["proportions"])
        self.client_order_id = str(order_params["client_order_id"])
        self.leverage_ratio = int(order_params["leverage_ratio"])
        self.tg_chatgrp = int(order_params["tg_chatgrp"])

        ##########################

        if self.clip_size_type == "BASE":
            self.symbol = self.base_ticker
        elif self.clip_size_type == "QUOTE":
            self.symbol = self.quote_ticker

        print(f"BYBIT {self.bybit_symbol} TWAP {self.direction} order")
        print(f"total trade size = {self.total_trade_size} {self.symbol}")
        print(f"order size on based on {self.clip_size_type} currency")
        print("conducting some checks")
        print("\n")

        ##############################
        ### conducting some checks ###
        ##############################

        ### check on number of clips ###
        # choose a time and interval such that clips are clips are integers
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

        ### checking on bybit_symbol ###
        # checking on ticker step size and round clip to that decimal place
        if self.bybit_symbol != self.base_ticker + self.quote_ticker:
            print("please check on base and quote ticker")
            print("symbols does not match")
            self.trading_check_counter += 1
            return None

        ### gets tick size for ticker ###
        df_symbol_info = self.get_ticker_info(self.bybit_symbol)
        if not df_symbol_info.empty:
            lot_size = df_symbol_info["basePrecision"].values[0]
            step_size = float(lot_size)
            self.decimal_place_ticker = int(math.log(1 / step_size, 10))
            # print(decimal_place)
            self.clip_size = round(
                self.total_trade_size / self.number_of_clips, self.decimal_place_ticker
            )
            print(f"clip size = {self.clip_size} {self.symbol}")
        else:
            print("please check on bybit symbol - it does not exist")
            self.trading_check_counter += 1
            return None

        ### check on randomizer ###
        time_interval_seconds = self.time_interval_seconds
        number_of_clips = self.total_twap_time_seconds / self.time_interval_seconds

        # preset clip proportions
        self.proportioned_clip_sizes = self.generate_clip_sizes(
            number_of_clips,
            self.total_trade_size,
            self.proportions,
            self.decimal_place_ticker,
        )
        print("\n")

        # randomizing sleep time
        self.randomized_sleep_time = self.randomizer(
            number_of_clips,
            time_interval_seconds * (1 - self.randomizer_bounds),
            time_interval_seconds * (1 + self.randomizer_bounds),
            self.total_twap_time_seconds,
        )
        print("\n")

        if not self.proportioned_clip_sizes:
            print("check clip sizes")
            return
        elif not self.randomized_sleep_time:
            print("check sleep time")
            return

        ### check if clip value is greater than pre-set clip limit ###
        clip_value = self.get_coin_value(self.symbol) * self.clip_size
        print(f"clip value = {clip_value}")
        if clip_value > self.clip_value_limit:
            print(f"clip value exceeds limit of {self.clip_value_limit}")
            print("please adjust trade size or clip intervals")
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

        print(f"leverage ratio = {self.leverage_ratio}")

        ### cross margin netAsset can be negative
        acc_valuation = (
            base_asset_balance_val + quote_asset_balance_val
        )  # account valuation
        print(f"account free margin = {acc_valuation}")

        # uses account valuation
        total_uta_acc_valuation = acc_valuation * self.leverage_ratio
        print(
            f"{self.bybit_symbol} cross margin acc free margin with {self.leverage_ratio} x leverage = {total_uta_acc_valuation}"
        )

        self.ticker_current_price = float(
            self.get_tickers(
                {
                    "category": "spot",
                    "symbol": f"{self.bybit_symbol.upper()}",
                }
            )["result"]["list"][0]["lastPrice"]
        )

        # get_coin_value
        if self.direction == "BUY" and self.clip_size_type == "BASE":
            # check if sufficient account valuation
            self.required_balance = (
                self.get_coin_value(self.base_ticker) * self.total_trade_size
            )
            if total_uta_acc_valuation < self.required_balance:
                print("insufficient account valuation")
                self.trading_check_counter += 1
                return None

        elif self.direction == "BUY" and self.clip_size_type == "QUOTE":
            self.required_balance = (
                self.get_coin_value(self.quote_ticker) * self.total_trade_size
            )
            if total_uta_acc_valuation < self.required_balance:
                print("insufficient account valuation")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "BASE":
            self.required_balance = (
                self.get_coin_value(self.base_ticker) * self.total_trade_size
            )
            if total_uta_acc_valuation < self.required_balance:
                print("insufficient account valuation")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "QUOTE":
            self.required_balance = (
                self.get_coin_value(self.quote_ticker) * self.total_trade_size
            )
            if total_uta_acc_valuation < self.total_trade_size:
                print("insufficient account valuation")
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
                "category": "spot",
                "symbol": self.bybit_symbol,
                "isLeverage": "1",  # set to borrow
                "side": self.direction.lower(),  # lowercase
                "orderType": "Market",
            }

            # specifying base or quote orders only applicable for market orders for okx
            clip_size_type = self.clip_size_type
            if clip_size_type == "BASE":
                placing_order_params["marketUnit"] = "baseCoin"
            elif clip_size_type == "QUOTE":
                placing_order_params["marketUnit"] = "quoteCoin"

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

            # sending telegram message before starting algo
            try:
                self.send_message(
                    self.tg_chatgrp,
                    f"""
                    {self.fire_emoji*3}\
                    \nStarting BYBIT TWAP {self.direction} order for {self.bybit_symbol}\
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
                    start_time = time.time()
                    placing_order_params["orderLinkId"] = (
                        self.client_order_id + "_" + str(int(start_time)),
                    )

                    clip_size_randomized = self.proportioned_clip_sizes[i]
                    sleep_time_randomized = self.randomized_sleep_time[i]

                    # sets minumum of remaining qty or randomized size rounded down
                    # should fix last clip issue
                    rounded = (
                        math.floor(self.remaining_qty * 10**self.decimal_place_ticker)
                        / 10**self.decimal_place_ticker
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)

                    placing_order_params["qty"] = str(
                        clip_size_randomized
                    )  # order params
                    order = self.place_order(placing_order_params)  # placing order here
                    print(f"order: {order}")
                    self.logger.info(order)

                    order_id = order["result"]["orderId"]

                    # self.getmarketorder_fills -> baseqty, quoteqty, df_fills
                    (
                        base_fill_qty,
                        quote_fill_qty,
                        trade_record_df,
                    ) = self.get_order_fills(order_id, self.bybit_symbol)

                    clip_symbol = self.bybit_symbol
                    clip_orderid = order_id
                    clip_transact_time = trade_record_df["execTime"][0]
                    clip_direction = trade_record_df["side"][0]

                    self.cumulative_filled_qty_quote += float(quote_fill_qty)
                    self.cumulative_filled_qty_base += float(base_fill_qty)

                    if clip_size_type == "BASE":
                        self.remaining_qty -= float(base_fill_qty)
                    elif clip_size_type == "QUOTE":
                        self.remaining_qty -= float(quote_fill_qty)

                    if tg_counter % 1 == 0:
                        self.send_message(
                            self.tg_chatgrp,
                            f"""
                            clip {i+1} of {number_of_clips}:\
                            \nplatform = BYBIT\
                            \nsymbol = {clip_symbol}\
                            \norderId = {clip_orderid}\
                            \ntime = {clip_transact_time}\
                            \nside = {clip_direction}\
                            \nqty_filled_base = {base_fill_qty}\
                            \nqty_filled_quote = {quote_fill_qty}\
                            \ncumulative_qty_base = {self.cumulative_filled_qty_base}\
                            \ncumulative_qty_quote = {self.cumulative_filled_qty_quote}\
                            """,
                        )
                    print(f"clip {i+1} of {number_of_clips} done")

                    end_time = time.time()
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

                    try:
                        self.send_message_error(
                            self.tg_chatgrp,
                            f"{self.alarm_emoji} clip {i+1} error, retrying again {self.alarm_emoji}",
                        )  # tg message
                    except Exception as ex:
                        self.logger.exception(ex)
                        self.logger.warning(
                            "telegram exception: continuing with execution"
                        )

                    sleep_time = 0.5
                    time.sleep(sleep_time)
                    print(f"slept for {sleep_time} seconds")

            self.send_message(
                self.tg_chatgrp,
                f"""
                {self.fire_emoji*3}\
                \nBYBIT TWAP order completed please check\
                \n{self.fire_emoji*3}\
                """,
            )


if __name__ == "__main__":
    config_path = sys.argv[1]
    log_path = sys.argv[2] + dt.datetime.now().strftime("%Y-%m-%d") + "-"
    mode = sys.argv[3]
    trading_params = sys.argv[4]

    # config_path = "C:/Users/EdgarTan/Documents/Github/python/config/trade_execution_algos/bybit/bybit_spot_twap_market_otc.ini"
    # log_path = f"C:/Users/EdgarTan/Documents/Github/python/logs/trade_execution_algos/bybit/{dt.datetime.now().strftime('%Y-%m-%d')}-"
    # mode = "check"
    # trading_params = "btcusdt-params"

    cfg = ConfigSetter(config_path)
    MARKET_PARAMS = cfg.get_section_data(trading_params)

    # for saving logs
    FILENAME = MARKET_PARAMS["client_order_id"] + ".log"  # setting log file as orderid

    # initializing
    client = MarginTwapAlgoMarketOTC(
        apikey=BYBIT_MCA_LTP1_TRADE["api_key"],
        apisecret=BYBIT_MCA_LTP1_TRADE["api_secret"],
        file_path=log_path,
        file_name=FILENAME,
        save_mode="a",
    )

    if mode.lower() == "check":
        client.twap_order_checking(MARKET_PARAMS)
    elif mode.lower() == "trade":
        client.place_twap_order(MARKET_PARAMS)
