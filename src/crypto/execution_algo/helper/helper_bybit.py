"""
Helper Functions used in Trading Algos - Specifically for BYBIT
"""

import math
import time

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

    def get_spot_ticker_info(self, ticker: str) -> int:
        """
        returns information on ticker

        Args:
            ticker: 'BTCUSDT', 'ETHUSDT', etc...

        Returns:
            integer
        """
        response_exchange_info = Bybit.get_instruments_info(
            self, {"category": "spot", "symbol": ticker.upper()}
        )
        base_precision = response_exchange_info[BybitConstants.RESULT][
            BybitConstants.LIST
        ][0][BybitConstants.LOT_SIZE_FILTER][BybitConstants.BASE_PRECISION]
        decimal_place = int(math.log(1 / float(base_precision), 10))
        return decimal_place

    def get_spot_coin_price(self, symbol: str) -> float:
        """
        Args:
            symbol: 'BTC', 'ETH' ...

        gets ticker price for symbol against USDT
        """
        stablecoin_list = ["USDT", "USDC"]
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
                ref_price = price[BybitConstants.RESULT][BybitConstants.LIST][0][
                    BybitConstants.LAST_PRICE
                ]
            except Exception as error:
                print(error)
        return float(ref_price)

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
            elif clip_value < 1:
                print("clip value less than okx min trade size of 1 USD, please adjust")
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
                rounded = math.floor(
                    remaining_qty
                    * 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                ) / 10 ** self.get_spot_ticker_info(trading_params[Constants.TICKER])
                clip_size_randomized = min(clip_size_randomized, rounded)

                order_payload[BybitConstants.QUANTITY.value] = str(clip_size_randomized)
                if order_params[Constants.CLIP_TYPE].upper() == "BASE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "baseCoin"
                elif order_params[Constants.CLIP_TYPE].upper() == "QUOTE":
                    order_payload[BybitConstants.MARKET_UNIT.value] = "quoteCoin"

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
                clip_fill_qty_quote = float(order_details[BybitConstants.QUANTITY])
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
