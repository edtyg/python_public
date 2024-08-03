"""
Helper Functions used in Trading Algos - Specifically for binance
"""

import math
import time

import pandas as pd

from src.crypto.exchanges.binance.rest.binance_cross_margin import BinanceCrossMargin
from src.crypto.exchanges.binance.rest.binance_isolated_margin import (
    BinanceIsolatedMargin,
)
from src.crypto.exchanges.binance.rest.binance_spot import BinanceSpot
from src.crypto.execution_algo.helper.helper_algo import HelperAlgo
from src.crypto.execution_algo.tools.binance_constants import BinanceConstants
from src.crypto.execution_algo.tools.constants import Constants
from src.crypto.execution_algo.tools.telegram_messenger import TelegramMessenger
from src.libraries.logging.logger_client import LoggerClient


class HelperBinance(
    BinanceSpot,
    BinanceCrossMargin,
    BinanceIsolatedMargin,
    LoggerClient,
):
    """
    Helper class for trading algos
    """

    def __init__(self, api_key, api_secret, file_path, file_name, save_mode):
        BinanceSpot.__init__(self, api_key, api_secret)
        BinanceCrossMargin.__init__(self, api_key, api_secret)
        BinanceIsolatedMargin.__init__(self, api_key, api_secret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    def get_spot_ticker_info(self, ticker: str) -> int:
        """
        Args:
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        Returns:
            int -> e.g 5
        """
        response_exchange_info = BinanceSpot.get_exchange_information(
            self, {"symbol": ticker.upper()}
        )
        df_symbols = pd.DataFrame(response_exchange_info[BinanceConstants.SYMBOLS])
        data = df_symbols[BinanceConstants.FILTERS].values[0][1]
        step_size = data[BinanceConstants.STEP_SIZE]
        decimal_place = int(math.log(1 / float(step_size), 10))
        return decimal_place

    def get_spot_coin_price(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH' ...

        gets ticker price for symbol against USDT
        if symbol passed is a stablecoin itself -> returns 1

        Uses Spot price -> calls from Spot Library

        Returns:
            float -> e.g 65000.00
        """
        stablecoin_list = ["USDT", "USDC"]
        if symbol.upper() in stablecoin_list:
            price = 1
        else:
            try:
                price_response = BinanceSpot.get_symbol_price_ticker(
                    self, {"symbol": f"{symbol.upper()}USDT"}
                )
                price = price_response[BinanceConstants.PRICE]
            except Exception as e:
                print(e)
        return float(price)

    def get_spot_balance(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH', etc...

        Returns:
            float -> e.g 0.0003
        """
        balance = False
        while balance is False:
            try:
                spot_balance = BinanceSpot.post_user_asset(self)
                df_assets = pd.DataFrame(spot_balance)
                balance = df_assets.loc[
                    df_assets[BinanceConstants.ASSET] == symbol.upper(),
                    BinanceConstants.FREE,
                ]

                if not balance.empty:
                    bal = float(balance.values[0])
                else:
                    bal = 0
                balance = True

            except Exception as error:
                print(f"pulling balance error: {error} trying again")
                sleep_time = 1
                time.sleep(sleep_time)
        return bal

    def get_cross_margin_balance(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH', etc...

        Returns:
            float -> e.g 0.0003
        """

        balance = False
        while balance is False:
            try:
                cross_margin_balance = BinanceCrossMargin.get_cross_margin_details(self)
                assets = cross_margin_balance[BinanceConstants.USER_ASSETS.value]
                df_assets = pd.DataFrame(assets)
                bal = df_assets.loc[
                    df_assets[BinanceConstants.ASSET] == symbol.upper(),
                    BinanceConstants.NET_ASSET,
                ].values[0]
                balance = True

            except Exception as error:
                print(f"pulling balance error: {error} trying again")
                sleep_time = 1
                time.sleep(sleep_time)
        return float(bal)

    def twap_market_order(self, order_params: dict):
        """
        Helper to place Cross Margin TWAP Market orders
        Does some checks specific to this order before starting algo
        """
        trading_params = HelperAlgo.params_parser(order_params)

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

        # GET Randomized Clip counts & Randomized Sleep times
        trading_clips = HelperAlgo.randomize(
            number_of_values=trading_params[Constants.CLIP_COUNT],
            lower_bound=trading_params[Constants.CLIP_SIZE]
            * (1 - trading_params[Constants.RANDOMIZER]),
            upper_bound=trading_params[Constants.CLIP_SIZE]
            * (1 + trading_params[Constants.RANDOMIZER]),
            sum_values=trading_params[Constants.QUANTITY],
            rounding=self.get_spot_ticker_info(trading_params[Constants.TICKER]),
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

        print(f"randomized trading clip sizes = {trading_clips}")
        print(f"randomized trading sleep times = {sleeping_clips}")

        # 2 - check if number any of the randomized clips > pre set trading clip limit
        # and check if clip is > Binance minimum trade amt of 5 USD
        if trading_params[Constants.CLIP_TYPE].upper() == "BASE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.BASE_CURRENCY]
            )
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.QUOTE_CURRENCY]
            )

        for clip in trading_clips:
            clip_value = coin_value * clip
            if clip_value > trading_params[Constants.CLIP_LIMIT]:
                print(
                    f"clip value exceeds limit of {trading_params[Constants.CLIP_LIMIT]}"
                )
                print("please adjust trade size or clip intervals or clip limits")
                return

            ### check if min trade size is satisfied ###
            elif clip_value < 5:
                print(
                    "clip value less than binance min trade size of 5 USD, please adjust"
                )
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
            "symbol": trading_params[Constants.TICKER],
            "isIsolated": "FALSE",
            "side": trading_params[Constants.DIRECTION],
            "type": "MARKET",
            "newClientOrderId": trading_params[Constants.ORDER_ID],
            "sideEffectType": "MARGIN_BUY",
        }

        # Sending Mesage On Start
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
                rounded = math.floor(
                    remaining_qty
                    * 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                ) / 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                clip_size_randomized = min(clip_size_randomized, rounded)

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    order_payload["quantity"] = clip_size_randomized
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    order_payload["quoteOrderQty"] = clip_size_randomized

                # placing order here
                order = BinanceCrossMargin.post_margin_new_order(self, order_payload)
                print("order placed")
                print(order)

                if order[BinanceConstants.STATUS] != "FILLED":
                    time.sleep(0.1)
                    continue

                self.logger.info(order)
                clip_symbol = order[BinanceConstants.SYMBOL]
                clip_orderid = order[BinanceConstants.ORDER_ID]
                clip_transact_time = order[BinanceConstants.TRANSACT_TIME]
                clip_direction = order[BinanceConstants.SIDE]
                clip_fill_details = order[BinanceConstants.FILLS]
                clip_fill_qty_quote = float(
                    order[BinanceConstants.CUMULATIVE_QUOTE_QTY]
                )
                cumulative_filled_qty_quote += clip_fill_qty_quote

                clip_fill_qty_base = 0
                for f in clip_fill_details:
                    clip_fill_qty_base += float(f[BinanceConstants.QUANTITY])
                cumulative_filled_qty_base += clip_fill_qty_base

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    remaining_qty -= clip_fill_qty_base
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    remaining_qty -= clip_fill_qty_quote
                average_filled_price = round(
                    clip_fill_qty_quote / clip_fill_qty_base, 6
                )

                # sending tg message
                TelegramMessenger.send_message(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"""
                    clip {i+1} of {int(order_params[Constants.CLIP_COUNT])}:\
                    \nplatform = {order_params[Constants.EXCHANGE]}\
                    \nsymbol = {clip_symbol}\
                    \norderId = {clip_orderid}\
                    \ntime = {clip_transact_time}\
                    \nside = {clip_direction}\
                    \navg_px = {average_filled_price}\
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
        This is a short Hedging TWAP with a preset proportion
        usually 50% in the first window
        """
        trading_params = HelperAlgo.params_parser(order_params)

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

        # GET Randomized Clip counts & Randomized Sleep times
        trading_clips = HelperAlgo.generate_clip_sizes(
            clip_count=trading_params[Constants.CLIP_COUNT],
            total_sum=trading_params[Constants.QUANTITY],
            proportions=trading_params[Constants.OTC_EXECUTION_PROPORTIONS],
            rounding=self.get_spot_ticker_info(trading_params[Constants.TICKER]),
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
        elif trading_params[Constants.CLIP_TYPE].upper() == "QUOTE":
            coin_value = self.get_spot_coin_price(
                trading_params[Constants.QUOTE_CURRENCY]
            )

        for clip in trading_clips:
            clip_value = coin_value * clip
            if clip_value > trading_params[Constants.CLIP_LIMIT]:
                print(
                    f"clip value exceeds limit of {trading_params[Constants.CLIP_LIMIT]}"
                )
                print("please adjust trade size or clip intervals or clip limits")
                return

            ### check if min trade size is satisfied ###
            elif clip_value < 5:
                print(
                    "clip value less than binance min trade size of 5 USD, please adjust"
                )
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
            "symbol": trading_params[Constants.TICKER],
            "isIsolated": "FALSE",
            "side": trading_params[Constants.DIRECTION],
            "type": "MARKET",
            "newClientOrderId": trading_params[Constants.ORDER_ID],
            "sideEffectType": "MARGIN_BUY",
        }

        # Sending Mesage On Start
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
                rounded = math.floor(
                    remaining_qty
                    * 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                ) / 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                clip_size_randomized = min(clip_size_randomized, rounded)

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    order_payload["quantity"] = clip_size_randomized
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    order_payload["quoteOrderQty"] = clip_size_randomized

                # placing order here
                order = BinanceCrossMargin.post_margin_new_order(self, order_payload)
                print("order placed")
                print(order)

                if order[BinanceConstants.STATUS] != "FILLED":
                    time.sleep(0.1)
                    continue

                self.logger.info(order)
                clip_symbol = order[BinanceConstants.SYMBOL]
                clip_orderid = order[BinanceConstants.ORDER_ID]
                clip_transact_time = order[BinanceConstants.TRANSACT_TIME]
                clip_direction = order[BinanceConstants.SIDE]
                clip_fill_details = order[BinanceConstants.FILLS]
                clip_fill_qty_quote = float(
                    order[BinanceConstants.CUMULATIVE_QUOTE_QTY]
                )
                cumulative_filled_qty_quote += clip_fill_qty_quote

                clip_fill_qty_base = 0
                for f in clip_fill_details:
                    clip_fill_qty_base += float(f[BinanceConstants.QUANTITY])
                cumulative_filled_qty_base += clip_fill_qty_base

                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    remaining_qty -= clip_fill_qty_base
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    remaining_qty -= clip_fill_qty_quote
                average_filled_price = round(
                    clip_fill_qty_quote / clip_fill_qty_base, 6
                )

                # sending tg message
                TelegramMessenger.send_message(
                    trading_params[Constants.TELEGRAM_GROUP],
                    f"""
                    clip {i+1} of {int(order_params[Constants.CLIP_COUNT])}:\
                    \nplatform = {order_params[Constants.EXCHANGE]}\
                    \nsymbol = {clip_symbol}\
                    \norderId = {clip_orderid}\
                    \ntime = {clip_transact_time}\
                    \nside = {clip_direction}\
                    \navg_px = {average_filled_price}\
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
