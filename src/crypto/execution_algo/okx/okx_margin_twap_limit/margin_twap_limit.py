"""
Okx SPOT TWAP algo - Market orders
"""

import datetime as dt
import math
import random
import sys
import time

import pandas as pd

from keys.api_work.crypto_exchanges.okx import OKX_MCA_LTP1_TRADE
from src.crypto.exchanges.okx.rest.okx_client import Okx
from src.libraries.configparser.config_setter import ConfigSetter
from src.libraries.logging.logger_client import LoggerClient
from src.libraries.telegram.telegram_trade_execution import Telegram


class MarginTwapAlgoLimit(Okx, LoggerClient, Telegram):
    """
    Args:
        Okx (_type_): Okx spot client
        LoggerClient (_type_): logging client
        Telegram (_type_): telegram client
    """

    def __init__(self, apikey, apisecret, passphrase, file_path, file_name, save_mode):
        Okx.__init__(self, apikey, apisecret, passphrase)
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        Telegram.__init__(self)

        ### trading params ###
        self.base_ticker = None
        self.quote_ticker = None
        self.okx_symbol = None
        self.direction = None
        self.clip_size_type = None
        self.clip_value_limit = None
        self.total_trade_size = None
        self.total_twap_time_seconds = None
        self.time_interval_seconds = None
        self.client_order_id = None
        self.price = None
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

        self.remaining_time = None
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
            try:
                price = self.get_ticker({"instId": f"{symbol}-USDT"})["data"][0]["last"]
            except Exception as error:
                print(error)
        return float(price)

    def get_ticker_info(self, ticker: str):
        """
        returns infomation on ticker

        Args:
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        Returns:
            pd.DataFrame
        """
        exchange_info = self.get_instruments({"instType": "SPOT"})
        df_exchange_info = pd.DataFrame(exchange_info["data"])
        df_symbol_info = df_exchange_info.loc[df_exchange_info["instId"] == ticker]
        return df_symbol_info

    def get_spot_balance(self, symbol):
        """
        returns spot free balance for symbol

        Args:
            symbol: 'BTC', 'ETH', etc...

        Returns:
            float -> 100
        """
        balance = False
        while balance is False:
            try:
                spot_balance = self.get_balance_trading()
                df_assets = pd.DataFrame(spot_balance["data"][0]["details"])

                if df_assets.empty:
                    # base ccy and quote ccy both 0
                    bal = 0
                    balance = True
                else:
                    # have either base ccy or quote ccy balance
                    # one of which might be 0
                    balance = df_assets.loc[
                        df_assets["ccy"] == symbol.upper(), "availBal"
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

    def get_order_fills(self, order_id, instrument_id: str):
        """
        get fills by orderid
        need to sleep awhile before we retrieve order
        can have multiple fills per order
        """
        trade_fills = False
        while trade_fills is False:
            try:
                time.sleep(1)  # sleep first
                # if order has fills -> pull fill records
                # might not have data when u pull too fast
                trade_record = self.get_transaction_details_3d(
                    {
                        "instType": "SPOT",
                        "ordId": order_id,
                        "instId": instrument_id,
                    }
                )
                if trade_record["data"]:
                    # only logs if not empty
                    self.logger.info(trade_record)
                    print(trade_record)

                fills = trade_record["data"]
                df_fills = pd.DataFrame(fills)
                df_fills["quote_fill_qty"] = df_fills["fillPx"].astype(
                    "float"
                ) * df_fills["fillSz"].astype("float")
                base_fill_qty = df_fills["fillSz"].astype("float").sum()
                quote_fill_qty = df_fills["quote_fill_qty"].astype("float").sum()
                trade_fills = True  # exits loop only when trades pulled successfully
            except Exception as error:
                print(error)
                sleep_time = 0.5
                print(f"retrieving fills failed. Retrying in {sleep_time} seconds")
                time.sleep(sleep_time)
            else:
                print("retrieving fills successful")
        return [base_fill_qty, quote_fill_qty]

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
        self.okx_symbol = str(order_params["okx_symbol"].upper())
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
            print("quote ccy not allowed for limit orders")
            self.symbol = self.quote_ticker
            return

        print(f"OKX {self.okx_symbol} TWAP {self.direction} order")
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

        ### checking on okx_symbol ###
        # checking on ticker step size and round clip to that decimal place
        if self.okx_symbol != self.base_ticker + "-" + self.quote_ticker:
            print("please check on base and quote ticker")
            print("symbols does not match")
            self.trading_check_counter += 1
            return None

        df_symbol_info = self.get_ticker_info(self.okx_symbol)
        if not df_symbol_info.empty:
            lot_size = df_symbol_info["minSz"].values[0]
            step_size = float(lot_size)
            self.decimal_place_ticker = int(math.log(1 / step_size, 10))
            # print(decimal_place)
            self.clip_size = round(
                self.total_trade_size / self.number_of_clips, self.decimal_place_ticker
            )
            print(f"clip size = {self.clip_size} {self.symbol}")
        else:
            print("please check on okx symbol - it does not exist")
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

        ### check if we have sufficient balance for orders ###
        base_asset_balance = self.get_spot_balance(self.base_ticker)
        print(f"current {self.base_ticker} balance = {base_asset_balance}")
        base_asset_balance_val = (
            self.get_coin_value(self.base_ticker) * base_asset_balance
        )
        print(f"current {self.base_ticker} valuation = {base_asset_balance_val}")

        quote_asset_balance = self.get_spot_balance(self.quote_ticker)
        print(f"current {self.quote_ticker} balance = {quote_asset_balance}")
        quote_asset_balance_val = (
            self.get_coin_value(self.quote_ticker) * quote_asset_balance
        )
        print(f"current {self.quote_ticker} valuation = {quote_asset_balance_val}")
        print("\n")

        self.ticker_current_price = float(
            self.get_ticker({"instId": self.okx_symbol})["data"][0]["last"]
        )

        ### checking for sufficient balances for trade ###

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
                "instId": self.okx_symbol,
                "tdMode": "cross",
                "tag": self.client_order_id,
                "side": self.direction.lower(),  # lowercase
                "ordType": "ioc",
            }

            # set remaining quantity and time
            self.remaining_qty = self.total_trade_size
            self.remaining_time = self.total_twap_time_seconds

            # sending telegram message before starting algo
            try:
                self.send_message(
                    self.tg_chatgrp,
                    f"""
                    {self.fire_emoji*3}\
                    \nStarting OKX TWAP {self.direction} order for {self.okx_symbol}\
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
            order_status = True
            while order_status is True:
                try:
                    start_time = time.time()
                    clip_size_type = self.clip_size_type  # base ccy only

                    # calculates number of remaining clips
                    number_of_clips = max(
                        int(self.remaining_time // self.time_interval_seconds), 1
                    )
                    clip_size = round(
                        self.remaining_qty / number_of_clips, self.decimal_place_ticker
                    )

                    placing_order_params["sz"] = clip_size  # order params
                    last_traded_price = float(
                        self.get_ticker({"instId": self.okx_symbol})["data"][0]["last"]
                    )

                    ### okx limit price can't be too far of current price ###
                    if self.direction.lower() == "sell":
                        order_price = max(
                            last_traded_price * 0.99, float(order_params["price"])
                        )
                        placing_order_params["px"] = order_price
                    elif self.direction.lower() == "buy":
                        order_price = min(
                            last_traded_price * 1.01, float(order_params["price"])
                        )
                        placing_order_params["px"] = order_price

                    print(f"remaining time = {self.remaining_time}")
                    print(f"clip interval = {self.time_interval_seconds}")
                    print(f"remaining clips = {number_of_clips}")
                    print(f"remaining qty = {self.remaining_qty}")
                    print(f"clip size = {clip_size}")

                    # placing order here
                    print(placing_order_params)
                    order = self.place_order(placing_order_params)
                    print(order)

                    order_id = order["data"][0]["ordId"]
                    filled_amt = self.get_order_details(
                        {
                            "ordId": order_id,
                            "instId": self.okx_symbol,
                        }
                    )
                    if float(filled_amt["data"][0]["accFillSz"]) == 0:
                        print("No Fills")
                        time.sleep(1)
                        end_time = time.time()
                        self.remaining_time -= end_time - start_time
                        print(f"remaining time = {self.remaining_time}")

                        # exits loop at last clip
                        if number_of_clips == 1:
                            # exits loop
                            order_status = False
                        continue

                    self.logger.info(order)  # only logs order if it's filled
                    # self.getmarketorder_fills -> baseqty, quoteqty, df_fills
                    (
                        base_fill_qty,
                        quote_fill_qty,
                    ) = self.get_order_fills(order_id, self.okx_symbol)

                    clip_symbol = self.okx_symbol
                    clip_orderid = order_id
                    clip_transact_time = order["data"][0]["ts"]
                    clip_direction = self.direction

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
                            clip {i+1}:\
                            \nplatform = Okx\
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
                    print(f"clip {i+1} done")

                    end_time = time.time()
                    self.time_offset += end_time - start_time
                    time_sleep_offset = max(
                        0, self.time_interval_seconds - self.time_offset
                    )
                    self.remaining_time -= self.time_offset + time_sleep_offset

                    # exits loop at last clip
                    if number_of_clips == 1:
                        # exits loop
                        order_status = False

                    i += 1
                    tg_counter += 1
                    self.time_offset = 0  # reset offset time
                    print(f"sleeping for {time_sleep_offset} seconds")
                    time.sleep(time_sleep_offset)

                except Exception as error:
                    print(f"placing order error: {error}")
                    self.logger.exception(error)

                    end_time = time.time()
                    self.time_offset += end_time - start_time
                    self.remaining_time -= self.time_offset
                    print(f"remaining time = {self.remaining_time}")
                    self.time_offset = 0  # reset offset time

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

                    sleep_time = 1
                    time.sleep(sleep_time)
                    print(f"slept for {sleep_time} seconds")

            self.send_message(
                self.tg_chatgrp,
                f"""
                {self.fire_emoji*3}\
                \nOKX TWAP order completed please check\
                \n{self.fire_emoji*3}\
                """,
            )


if __name__ == "__main__":
    config_path = sys.argv[1]
    log_path = sys.argv[2] + dt.datetime.now().strftime("%Y-%m-%d") + "-"
    mode = sys.argv[3]
    trading_params = sys.argv[4]

    # config_path = "C:/Users/EdgarTan/Documents/Github/python/config/trade_execution_algos/okx/okx_margin_twap_limit.ini"
    # log_path = f"C:/Users/EdgarTan/Documents/Github/python/logs/trade_execution_algos/okx/{dt.datetime.now().strftime('%Y-%m-%d')}-"
    # mode = "trade"
    # trading_params = "tonusdt-level2-params"

    cfg = ConfigSetter(config_path)
    MARKET_PARAMS = cfg.get_section_data(trading_params)

    # # for saving logs
    FILENAME = MARKET_PARAMS["client_order_id"] + ".log"  # setting log file as orderid

    # initializing
    client = MarginTwapAlgoLimit(
        apikey=OKX_MCA_LTP1_TRADE["api_key"],
        apisecret=OKX_MCA_LTP1_TRADE["api_secret"],
        passphrase=OKX_MCA_LTP1_TRADE["passphrase"],
        file_path=log_path,
        file_name=FILENAME,
        save_mode="a",
    )

    if mode.lower() == "check":
        client.twap_order_checking(MARKET_PARAMS)
    elif mode.lower() == "trade":
        client.place_twap_order(MARKET_PARAMS)
