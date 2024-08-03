"""
Helper Functions used in Trading Algos - Specifically for BYBIT
"""

import math
import time
import traceback

import pandas as pd

from src.crypto.exchanges.bybit.rest.bybit_client import Bybit
from src.crypto.execution_algo.helper.helper_algo import HelperAlgo
from src.crypto.execution_algo.tools.bybit_constants import BybitConstants
from src.crypto.execution_algo.tools.constants import Constants
from src.crypto.execution_algo.tools.telegram_messenger import TelegramMessenger
from src.libraries.logging.logger_client import LoggerClient


class HelperBybit(
    Bybit,
    LoggerClient,
):
    """
    Helper class for trading algos
    """

    def __init__(self, api_key, api_secret, file_path, file_name, save_mode):
        Bybit.__init__(self, api_key, api_secret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    def get_ticker_info(self, category: str, ticker: str) -> dict:
        """
        returns information on ticker.

        Args:
            category: "spot", "linear", "inverse", "option"
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        Returns:
            dict of ticker info used in placing orders
            mainly spot for now

        """
        if category not in [
            BybitConstants.SPOT,
            BybitConstants.LINEAR,
            BybitConstants.INVERSE,
            BybitConstants.OPTION,
        ]:
            print("category not valid, please select valid category")
            return

        instrument_info = Bybit.get_instruments_info(
            self,
            {
                BybitConstants.CATEGORY: category,
                BybitConstants.SYMBOL: ticker.upper(),
            },
        )

        if category == BybitConstants.SPOT:
            data = instrument_info[BybitConstants.RESULT][BybitConstants.LIST][0]
            base_ccy_precision = data[BybitConstants.LOT_SIZE_FILTER][
                BybitConstants.BASE_PRECISION
            ]
            quote_ccy_precision = data[BybitConstants.LOT_SIZE_FILTER][
                BybitConstants.QUOTE_PRECISION
            ]
            min_order_amt = data[BybitConstants.LOT_SIZE_FILTER][
                BybitConstants.MIN_ORDER_AMT
            ]
            min_order_qty = data[BybitConstants.LOT_SIZE_FILTER][
                BybitConstants.MIN_ORDER_QTY
            ]
            price_precision = data[BybitConstants.PRICE_FILTER][
                BybitConstants.TICK_SIZE
            ]

            base_ccy_dp = abs(round(math.log(float(base_ccy_precision), 10)))
            quote_ccy_dp = abs(round(math.log(float(quote_ccy_precision), 10)))
            price_dp = abs(round(math.log(float(price_precision), 10)))

            spot_dict = {
                "base_ccy_dp": int(base_ccy_dp),
                "quote_ccy_dp": int(quote_ccy_dp),
                "min_order_amt": float(min_order_amt),  # quote_ccy
                "min_order_qty": float(min_order_qty),  # base_ccy
                "price_dp": price_dp,
            }
            return spot_dict
        else:
            # to add on for liner and inverse if required
            return

    def get_spot_coin_price(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH' ...

        gets ticker price for symbol against USDT
        """
        stablecoin_list = ["USDT", "USDC"]
        if symbol in stablecoin_list:
            price = 1
        else:
            try:
                ticker_price = self.get_tickers(
                    {
                        BybitConstants.CATEGORY: BybitConstants.SPOT,
                        BybitConstants.SYMBOL: f"{symbol.upper()}USDT",
                    }
                )
                price = ticker_price[BybitConstants.RESULT][BybitConstants.LIST][0][
                    BybitConstants.LAST_PRICE
                ]
            except KeyError as error:
                print(error)
        return float(price)

    def get_spot_balance(self, symbol: str) -> float:
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
                unified_account_balance = self.get_all_coins_balance(
                    {
                        BybitConstants.ACCOUNT_TYPE: BybitConstants.UNIFIED,
                        BybitConstants.COIN: symbol.upper(),
                    }
                )
                balance = unified_account_balance[BybitConstants.RESULT][
                    BybitConstants.BALANCE
                ]
                df_balance = pd.DataFrame(balance)

                if df_balance.empty:
                    bal = 0
                    balance = True
                else:
                    balance = df_balance.loc[
                        df_balance[BybitConstants.COIN] == symbol.upper(),
                        BybitConstants.WALLET_BALANCE,
                    ]

                    if balance.size > 0:
                        bal = float(balance.values[0])
                    else:
                        bal = 0
            except KeyError as error:
                print(f"pulling balance error: {error} pulling again")
                sleep_time = 1
                time.sleep(sleep_time)
        return bal

    def twap_market_order(self, order_params: dict):
        """
        Helper to place Cross Margin TWAP Market orders
        Does some checks specific to this order before starting algo
        """
        trading_params = HelperAlgo.params_parser(order_params)
        ticker_info = self.get_ticker_info(
            BybitConstants.SPOT, trading_params[Constants.TICKER]
        )

        # 1 - Check on number of clips
        print(f"number of clips = {trading_params[Constants.CLIP_COUNT]}")
        print(
            f"clip intervals = {trading_params[Constants.TWAP_CLIP_INTERVAL]} seconds"
        )

        if (
            int(trading_params[Constants.CLIP_COUNT])
            != trading_params[Constants.CLIP_COUNT]
        ):
            print("Please choose a different TWAP time and interval")
            return

        # Randomized Clip counts
        if trading_params[Constants.CLIP_TYPE].upper() == "BASE":
            trading_clips = HelperAlgo.randomize(
                number_of_values=trading_params[Constants.CLIP_COUNT],
                lower_bound=trading_params[Constants.CLIP_SIZE]
                * (1 - trading_params[Constants.RANDOMIZER]),
                upper_bound=trading_params[Constants.CLIP_SIZE]
                * (1 + trading_params[Constants.RANDOMIZER]),
                sum_values=trading_params[Constants.QUANTITY],
                rounding=ticker_info["base_ccy_dp"],
            )
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            trading_clips = HelperAlgo.randomize(
                number_of_values=trading_params[Constants.CLIP_COUNT],
                lower_bound=trading_params[Constants.CLIP_SIZE]
                * (1 - trading_params[Constants.RANDOMIZER]),
                upper_bound=trading_params[Constants.CLIP_SIZE]
                * (1 + trading_params[Constants.RANDOMIZER]),
                sum_values=trading_params[Constants.QUANTITY],
                rounding=ticker_info["quote_ccy_dp"],
            )

        # Randomized Sleep times
        sleeping_clips = HelperAlgo.randomize(
            number_of_values=trading_params[Constants.CLIP_COUNT],
            lower_bound=trading_params[Constants.TWAP_CLIP_INTERVAL]
            * (1 - trading_params[Constants.RANDOMIZER]),
            upper_bound=trading_params[Constants.TWAP_CLIP_INTERVAL]
            * (1 + trading_params[Constants.RANDOMIZER]),
            sum_values=trading_params[Constants.TWAP_DURATION],
            rounding=2,
        )

        print(f"randomized trading clip sizes = {trading_clips}")
        print(f"randomized trading sleep times = {sleeping_clips}")

        # 2 - check if number any of the randomized clips exceeds pre-set clip limits
        # or if clip size is lower than min trade amt
        if trading_params[Constants.CLIP_TYPE].upper() == "BASE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.BASE_CURRENCY]
            )
            min_order_amt = ticker_info["min_order_qty"]
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.QUOTE_CURRENCY]
            )
            min_order_amt = ticker_info["min_order_amt"]

        for clip in trading_clips:
            clip_value = coin_value * clip
            if clip_value > trading_params[Constants.CLIP_LIMIT]:
                print(
                    f"clip value exceeds limit of {trading_params[Constants.CLIP_LIMIT]}"
                )
                print("please adjust trade size or clip intervals or clip limits")
                return

            ### check if min trade size is satisfied ###
            elif clip < min_order_amt:
                print("clip amount less than minimum required")
                return

        if trading_params[Constants.TRADE_STATUS].upper() not in ["CHECK", "TRADE"]:
            print("check on trade status -> has to be either check or trade")
            return
        elif trading_params[Constants.TRADE_STATUS].upper() == "CHECK":
            print("all checks passed")
            print("select trade mode to begin algo")
            return

        # proceeding to trading algo here
        print("trade mode selected -> proceeding with trading algo")

        order_payload = {
            "category": "spot",
            "symbol": trading_params[Constants.TICKER],
            "isLeverage": "1",  # set to borrow
            "side": trading_params[Constants.DIRECTION].lower(),
            "orderType": "Market",
        }

        # Sending Message On Start
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \nStarting {trading_params[Constants.EXCHANGE]} {trading_params[Constants.ALGO_TYPE]} {trading_params[Constants.DIRECTION]} order for {trading_params[Constants.TICKER]}\
            \ntotal size = {trading_params[Constants.QUANTITY]} {trading_params[Constants.CLIP_CCY]} \
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )

        # set remaining qty
        i = 0
        remaining_qty = trading_params[Constants.QUANTITY]
        cumulative_filled_qty_base = 0
        cumulative_filled_qty_quote = 0
        clip_runtime = 0  # measures time taken for each iteration
        while i < int(trading_params[Constants.CLIP_COUNT]):
            try:
                start_time = time.time()  # start time
                clip_size_randomized = trading_clips[i]
                sleep_time_randomized = sleeping_clips[i]

                # sets minumum of remaining qty or randomized size rounded down
                # should fix rounding issues of last clip
                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "baseCoin"
                    rounded = HelperAlgo.floor_amount(
                        remaining_qty, ticker_info["base_ccy_dp"]
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)
                    order_payload[BybitConstants.QUANTITY.value] = (
                        f"{clip_size_randomized:.{ticker_info['base_ccy_dp']}f}"
                    )

                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "quoteCoin"
                    rounded = HelperAlgo.floor_amount(
                        remaining_qty, ticker_info["quote_ccy_dp"]
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)
                    order_payload[BybitConstants.QUANTITY.value] = (
                        f"{clip_size_randomized:.{ticker_info['quote_ccy_dp']}f}"
                    )

                # placing order here
                print(order_payload)
                order = HelperBybit.place_order(self, order_payload)
                print("order placed")
                print(order)

                try:
                    order_id = order["result"]["orderId"]
                except Exception as error:
                    print(error)
                    print("order failed -> no order id returned")
                    print("continuing on next order")
                    continue

                self.logger.info(order)  # logs if order is successful
                order_details = HelperBybit.get_order_history(
                    self,
                    {
                        "category": "spot",
                        "symbol": order_params[Constants.TICKER],
                        "orderId": order_id,
                    },
                )[BybitConstants.RESULT][BybitConstants.LIST][0]
                clip_symbol = order_details[BybitConstants.SYMBOL]
                clip_transact_time = order_details[BybitConstants.UPDATED_TIME]
                clip_direction = order_details[BybitConstants.SIDE]
                clip_fill_qty_base = float(
                    order_details[BybitConstants.CUMULATIVE_BASE]
                )
                clip_fill_qty_quote = float(
                    order_details[BybitConstants.CUMULATIVE_QUOTE]
                )
                clip_avg_price = float(order_details[BybitConstants.AVERAGE_PRICE])
                cumulative_filled_qty_base += clip_fill_qty_base
                cumulative_filled_qty_quote += clip_fill_qty_quote

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    remaining_qty -= clip_fill_qty_base
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    remaining_qty -= clip_fill_qty_quote

                # sending tg message
                TelegramMessenger.send_message(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"""
                    clip {i+1} of {int(order_params[Constants.CLIP_COUNT])}:\
                    \nplatform = {order_params[Constants.EXCHANGE]}\
                    \nsymbol = {clip_symbol}\
                    \norderId = {order_id}\
                    \ntime = {clip_transact_time}\
                    \nside = {clip_direction}\
                    \navg_px = {clip_avg_price}\
                    \nqty_filled_base = {clip_fill_qty_base}\
                    \nqty_filled_quote = {clip_fill_qty_quote}\
                    \ncumulative_qty_base = {cumulative_filled_qty_base}\
                    \ncumulative_qty_quote = {cumulative_filled_qty_quote}\
                    """,
                )
                print(f"clip {i+1} of {int(trading_params[Constants.CLIP_COUNT])} done")
                end_time = time.time()  # end time
                clip_runtime = end_time - start_time  # time taken to run this clip

                # offset twap clip duration by runtime of each clip
                time_sleep_offset = max(0, sleep_time_randomized - clip_runtime)
                print(f"sleeping for {time_sleep_offset} seconds")
                time.sleep(time_sleep_offset)

                i += 1  # move to next clip
            except Exception as error:
                print(f"placing order error: {error}")
                self.logger.exception(error)

                # sending tg message
                TelegramMessenger.send_message_error(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"{TelegramMessenger.alarm_emoji} clip {i+1} error, retrying again {TelegramMessenger.alarm_emoji}",
                )
                self.logger.warning("telegram exception: continuing with execution")

                sleep_time = 0.2
                time.sleep(sleep_time)
                print(f"Error slept for {sleep_time} seconds")

        # send message on completion
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \norder completed please check\
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )

    def twap_market_otc_order(self, order_params: dict):
        """
        Helper to place Cross Margin TWAP Market OTC orders
        Does some checks specific to this order before starting algo
        """
        trading_params = HelperAlgo.params_parser(order_params)
        ticker_info = self.get_ticker_info(
            BybitConstants.SPOT, trading_params[Constants.TICKER]
        )

        # 1 - Check on number of clips
        print(f"number of clips = {trading_params[Constants.CLIP_COUNT]}")
        print(
            f"clip intervals = {trading_params[Constants.TWAP_CLIP_INTERVAL]} seconds"
        )

        if (
            int(trading_params[Constants.CLIP_COUNT])
            != trading_params[Constants.CLIP_COUNT]
        ):
            print("Please choose a different TWAP time and interval")
            return

        # Randomized Clip counts
        if trading_params[Constants.CLIP_TYPE].upper() == "BASE":
            trading_clips = HelperAlgo.generate_clip_sizes(
                clip_count=trading_params[Constants.CLIP_COUNT],
                total_sum=trading_params[Constants.QUANTITY],
                proportions=trading_params[Constants.OTC_EXECUTION_PROPORTIONS],
                rounding=ticker_info["base_ccy_dp"],
            )
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            trading_clips = HelperAlgo.generate_clip_sizes(
                clip_count=trading_params[Constants.CLIP_COUNT],
                total_sum=trading_params[Constants.QUANTITY],
                proportions=trading_params[Constants.OTC_EXECUTION_PROPORTIONS],
                rounding=ticker_info["quote_ccy_dp"],
            )

        sleeping_clips = HelperAlgo.randomize(
            number_of_values=trading_params[Constants.CLIP_COUNT],
            lower_bound=trading_params[Constants.TWAP_CLIP_INTERVAL]
            * (1 - trading_params[Constants.RANDOMIZER]),
            upper_bound=trading_params[Constants.TWAP_CLIP_INTERVAL]
            * (1 + trading_params[Constants.RANDOMIZER]),
            sum_values=trading_params[Constants.TWAP_DURATION],
            rounding=2,
        )

        print(f"OTC Hedging trading clip sizes = {trading_clips}")
        print(f"randomized trading sleep times = {sleeping_clips}")

        # 2 - check if number any of the randomized clips > pre set trading clip limit
        # and check if clip is > Binance minimum trade amt of 5 USD
        if trading_params[Constants.CLIP_TYPE].upper() == "BASE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.BASE_CURRENCY]
            )
            min_order_amt = ticker_info["min_order_qty"]
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.QUOTE_CURRENCY]
            )
            min_order_amt = ticker_info["min_order_amt"]

        for clip in trading_clips:
            clip_value = coin_value * clip
            if clip_value > trading_params[Constants.CLIP_LIMIT]:
                print(
                    f"clip value exceeds limit of {trading_params[Constants.CLIP_LIMIT]}"
                )
                print("please adjust trade size or clip intervals or clip limits")
                return

            ### check if min trade size is satisfied ###
            elif clip < min_order_amt:
                print("clip amount less than minimum required")
                return

        if trading_params[Constants.TRADE_STATUS].upper() not in ["CHECK", "TRADE"]:
            print("check on trade status -> has to be either check or trade")
            return
        elif trading_params[Constants.TRADE_STATUS].upper() == "CHECK":
            print("all checks passed")
            print("select trade mode to begin algo")
            return

        # proceeding to trading algo here
        print("trade mode selected -> proceeding with trading algo")

        order_payload = {
            "category": "spot",
            "symbol": trading_params[Constants.TICKER],
            "isLeverage": "1",  # set to borrow
            "side": trading_params[Constants.DIRECTION].lower(),
            "orderType": "Market",
        }

        # Sending Message On Start
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \nStarting {trading_params[Constants.EXCHANGE]} {trading_params[Constants.ALGO_TYPE]} {trading_params[Constants.DIRECTION]} order for {trading_params[Constants.TICKER]}\
            \ntotal size = {trading_params[Constants.QUANTITY]} {trading_params[Constants.CLIP_CCY]} \
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )

        # set remaining qty
        i = 0
        remaining_qty = trading_params[Constants.QUANTITY]
        cumulative_filled_qty_base = 0
        cumulative_filled_qty_quote = 0
        clip_runtime = 0  # measures time taken for each iteration
        while i < int(trading_params[Constants.CLIP_COUNT]):
            try:
                start_time = time.time()  # start time
                clip_size_randomized = trading_clips[i]
                sleep_time_randomized = sleeping_clips[i]

                # sets minumum of remaining qty or randomized size rounded down
                # should fix rounding issues of last clip
                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "baseCoin"
                    rounded = HelperAlgo.floor_amount(
                        remaining_qty, ticker_info["base_ccy_dp"]
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)
                    order_payload[BybitConstants.QUANTITY.value] = (
                        f"{clip_size_randomized:.{ticker_info['base_ccy_dp']}f}"
                    )

                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "quoteCoin"
                    rounded = HelperAlgo.floor_amount(
                        remaining_qty, ticker_info["quote_ccy_dp"]
                    )
                    clip_size_randomized = min(clip_size_randomized, rounded)
                    order_payload[BybitConstants.QUANTITY.value] = (
                        f"{clip_size_randomized:.{ticker_info['quote_ccy_dp']}f}"
                    )

                # placing order here
                print(order_payload)
                order = HelperBybit.place_order(self, order_payload)
                print("order placed")
                print(order)

                try:
                    order_id = order["result"]["orderId"]
                except Exception as error:
                    print(error)
                    print("order failed -> no order id returned")
                    print("continuing on next order")
                    continue

                self.logger.info(order)  # logs if order is successful
                order_details = HelperBybit.get_order_history(
                    self,
                    {
                        "category": "spot",
                        "symbol": order_params[Constants.TICKER],
                        "orderId": order_id,
                    },
                )[BybitConstants.RESULT][BybitConstants.LIST][0]
                clip_symbol = order_details[BybitConstants.SYMBOL]
                clip_transact_time = order_details[BybitConstants.UPDATED_TIME]
                clip_direction = order_details[BybitConstants.SIDE]
                clip_fill_qty_base = float(
                    order_details[BybitConstants.CUMULATIVE_BASE]
                )
                clip_fill_qty_quote = float(
                    order_details[BybitConstants.CUMULATIVE_QUOTE]
                )
                clip_avg_price = float(order_details[BybitConstants.AVERAGE_PRICE])
                cumulative_filled_qty_base += clip_fill_qty_base
                cumulative_filled_qty_quote += clip_fill_qty_quote

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    remaining_qty -= clip_fill_qty_base
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    remaining_qty -= clip_fill_qty_quote

                # sending tg message
                TelegramMessenger.send_message(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"""
                    clip {i+1} of {int(order_params[Constants.CLIP_COUNT])}:\
                    \nplatform = {order_params[Constants.EXCHANGE]}\
                    \nsymbol = {clip_symbol}\
                    \norderId = {order_id}\
                    \ntime = {clip_transact_time}\
                    \nside = {clip_direction}\
                    \navg_px = {clip_avg_price}\
                    \nqty_filled_base = {clip_fill_qty_base}\
                    \nqty_filled_quote = {clip_fill_qty_quote}\
                    \ncumulative_qty_base = {cumulative_filled_qty_base}\
                    \ncumulative_qty_quote = {cumulative_filled_qty_quote}\
                    """,
                )
                print(f"clip {i+1} of {int(trading_params[Constants.CLIP_COUNT])} done")
                end_time = time.time()  # end time
                clip_runtime = end_time - start_time  # time taken to run this clip

                # offset twap clip duration by runtime of each clip
                time_sleep_offset = max(0, sleep_time_randomized - clip_runtime)
                print(f"sleeping for {time_sleep_offset} seconds")
                time.sleep(time_sleep_offset)

                i += 1  # move to next clip
            except Exception as error:
                print(f"placing order error: {error}")
                self.logger.exception(error)

                # sending tg message
                TelegramMessenger.send_message_error(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"{TelegramMessenger.alarm_emoji} clip {i+1} error, retrying again {TelegramMessenger.alarm_emoji}",
                )
                self.logger.warning("telegram exception: continuing with execution")

                sleep_time = 0.2
                time.sleep(sleep_time)
                print(f"Error slept for {sleep_time} seconds")

        # send message on completion
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \norder completed please check\
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )

    def twap_limit_order(self, order_params: dict):
        """
        Helper to place Cross Margin TWAP Limit IOC orders
        Does some checks specific to this order before starting algo
        Places IOC Limit orders at specified prices
        """
        trading_params = HelperAlgo.params_parser(order_params)
        ticker_info = self.get_ticker_info(
            BybitConstants.SPOT, trading_params[Constants.TICKER]
        )

        # 1 - Check on number of clips
        print(f"number of clips = {trading_params[Constants.CLIP_COUNT]}")
        print(
            f"clip intervals = {trading_params[Constants.TWAP_CLIP_INTERVAL]} seconds"
        )

        if (
            int(trading_params[Constants.CLIP_COUNT])
            != trading_params[Constants.CLIP_COUNT]
        ):
            print("Please choose a different TWAP time and interval")
            return

        # 2 - Check if Clip type is Base or Quote CCY - Limit orders only allow base ccy
        if trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            print("Adjust Clip Type, Limit Orders does not allow Quote CCY")
            return

        if trading_params[Constants.TRADE_STATUS].upper() not in ["CHECK", "TRADE"]:
            print("check on trade status -> has to be either check or trade")
            return
        elif trading_params[Constants.TRADE_STATUS].upper() == "CHECK":
            print("all checks passed")
            print("select trade mode to begin algo")
            return

        if trading_params[Constants.TRADE_STATUS].upper() not in ["CHECK", "TRADE"]:
            print("check on trade status -> has to be either check or trade")
            return
        elif trading_params[Constants.TRADE_STATUS].upper() == "CHECK":
            print("all checks passed")
            print("select trade mode to begin algo")
            return

        # proceeding to trading algo here
        print("trade mode selected -> proceeding with trading algo")

        order_payload = {
            "category": "spot",
            "symbol": trading_params[Constants.TICKER],
            "isLeverage": "1",  # set to borrow
            "side": trading_params[Constants.DIRECTION].lower(),
            "orderType": "Limit",
            "timeInForce": "IOC",
        }

        # Sending Message On Start
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \nStarting {trading_params[Constants.EXCHANGE]} {trading_params[Constants.ALGO_TYPE]} {trading_params[Constants.DIRECTION]} order for {trading_params[Constants.TICKER]}\
            \ntotal size = {trading_params[Constants.QUANTITY]} {trading_params[Constants.CLIP_CCY]} \
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )

        # set remaining qty
        i = 0
        remaining_qty = trading_params[Constants.QUANTITY]
        remaining_time = trading_params[Constants.TWAP_DURATION]
        cumulative_filled_qty_base = 0
        cumulative_filled_qty_quote = 0
        clip_runtime = 0  # measures time taken for each iteration
        rounding = ticker_info["base_ccy_dp"]  # base ccy only for limit orders
        order_status = True
        while order_status is True:
            try:
                start_time = time.time()  # start time

                # calculates number of remaining clips -> Remaining time / clip interval
                number_of_clips = max(
                    int(remaining_time // trading_params[Constants.TWAP_CLIP_INTERVAL]),
                    1,
                )
                clip_size = round(
                    remaining_qty / number_of_clips,
                    rounding,
                )
                order_payload["qty"] = str(clip_size)  # order params
                last_traded_price = self.get_tickers(
                    {"category": "spot", "symbol": trading_params[Constants.TICKER]}
                )
                last_traded_price = float(
                    last_traded_price[BybitConstants.RESULT][BybitConstants.LIST][0][
                        BybitConstants.LAST_PRICE
                    ]
                )

                ### Bybit limit price can't be > 3% frm mkt px as taker ###
                # sell at last traded price offset 1%
                # order might not be filled if i send at last traded px
                if trading_params[Constants.DIRECTION].upper() == "SELL":
                    order_price = max(
                        last_traded_price * 0.99, float(order_params["price"])
                    )
                    order_payload["price"] = str(
                        round(order_price, ticker_info["price_dp"])
                    )
                elif trading_params[Constants.DIRECTION].upper() == "BUY":
                    order_price = min(
                        last_traded_price * 1.01, float(order_params["price"])
                    )
                    order_payload["price"] = str(
                        round(order_price, ticker_info["price_dp"])
                    )

                # placing order here
                print(order_payload)
                order = HelperBybit.place_order(self, order_payload)
                print("order placed")
                print(order)

                try:
                    # if no order ID retrieved from order response
                    # Order did not go through -> move to next iteration
                    order_id = order["result"]["orderId"]
                except Exception as error:
                    print(error)
                    print("Limit order failed -> no order id returned")
                    print("continuing on next order")
                    time.sleep(1)
                    end_time = time.time()
                    remaining_time -= end_time - start_time
                    print(f"remaining time = {remaining_time}")

                    if number_of_clips == 1:
                        # exits loop
                        order_status = False
                    continue

                self.logger.info(order)  # logs if order is successful
                retrieve_order_status = False
                while retrieve_order_status is False:
                    try:
                        # bybit server requires some time for order to be retrievable
                        time.sleep(1)
                        order_details = HelperBybit.get_order_history(
                            self,
                            {
                                "category": "spot",
                                "symbol": order_params[Constants.TICKER],
                                "orderId": order_id,
                            },
                        )[BybitConstants.RESULT][BybitConstants.LIST][0]
                        retrieve_order_status = True
                    except Exception as e:
                        print(e)
                        print("trying to retrieve order details")
                print(order_details)

                if (
                    float(order_details[BybitConstants.CUMULATIVE_BASE]) == 0
                    or float(order_details[BybitConstants.CUMULATIVE_QUOTE]) == 0
                ):
                    print("No Fills")
                    time.sleep(1)
                    end_time = time.time()
                    remaining_time -= end_time - start_time
                    print(f"remaining time = {remaining_time}")

                    # exits loop at last clip
                    if number_of_clips == 1:
                        # exits loop
                        order_status = False
                    continue

                clip_symbol = order_details[BybitConstants.SYMBOL]
                clip_transact_time = order_details[BybitConstants.UPDATED_TIME]
                clip_direction = order_details[BybitConstants.SIDE]
                clip_fill_qty_base = float(
                    order_details[BybitConstants.CUMULATIVE_BASE]
                )
                clip_fill_qty_quote = float(
                    order_details[BybitConstants.CUMULATIVE_QUOTE]
                )
                if order_details[BybitConstants.AVERAGE_PRICE] == "":
                    # no fills for IOC order
                    clip_avg_price = 0
                else:
                    clip_avg_price = float(order_details[BybitConstants.AVERAGE_PRICE])
                cumulative_filled_qty_base += clip_fill_qty_base
                cumulative_filled_qty_quote += clip_fill_qty_quote

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    remaining_qty -= clip_fill_qty_base
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    remaining_qty -= clip_fill_qty_quote

                if clip_fill_qty_base == 0 or clip_fill_qty_quote == 0:
                    print("No fills")
                    time.sleep(1)
                    end_time = time.time()
                    remaining_time -= end_time - start_time
                    print(f"remaining time = {remaining_time}")

                    # exits loop at last clip
                    if number_of_clips == 1:
                        # exits loop
                        order_status = False
                    continue

                # sending tg message
                TelegramMessenger.send_message(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"""
                    clip {i+1}:\
                    \nplatform = {order_params[Constants.EXCHANGE]}\
                    \nsymbol = {clip_symbol}\
                    \norderId = {order_id}\
                    \ntime = {clip_transact_time}\
                    \nside = {clip_direction}\
                    \navg_px = {clip_avg_price}\
                    \nqty_filled_base = {clip_fill_qty_base}\
                    \nqty_filled_quote = {clip_fill_qty_quote}\
                    \ncumulative_qty_base = {cumulative_filled_qty_base}\
                    \ncumulative_qty_quote = {cumulative_filled_qty_quote}\
                    """,
                )
                print(f"clip {i+1} done")
                end_time = time.time()  # end time
                clip_runtime = end_time - start_time  # time taken to run this clip

                # offset twap clip duration by runtime of each clip
                time_sleep_offset = max(
                    0, trading_params[Constants.TWAP_CLIP_INTERVAL] - clip_runtime
                )
                remaining_time -= clip_runtime + time_sleep_offset

                # exits loop at last clip
                if number_of_clips == 1:
                    # exits loop
                    order_status = False

                print(f"Remaining Time = {remaining_time}")
                print(f"Remaining Quantity = {remaining_qty}")

                i += 1  # move to next clip
                print(f"sleeping for {time_sleep_offset} seconds")
                time.sleep(time_sleep_offset)

            except Exception as error:
                print(f"placing order error: {error}")
                self.logger.exception(error)

                # sending tg message
                TelegramMessenger.send_message_error(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"{TelegramMessenger.alarm_emoji} clip {i+1} error, retrying again {TelegramMessenger.alarm_emoji}",
                )
                self.logger.warning("telegram exception: continuing with execution")

                sleep_time = 0.2
                time.sleep(sleep_time)
                print(f"Error slept for {sleep_time} seconds")
                traceback.print_exc()

        # send message on completion
        TelegramMessenger.send_message(
            trading_params[Constants.TELEGRAM_GROUP],
            f"""
            {TelegramMessenger.fire_emoji*3}\
            \norder completed please check\
            \n{TelegramMessenger.fire_emoji*3}\
            """,
        )
