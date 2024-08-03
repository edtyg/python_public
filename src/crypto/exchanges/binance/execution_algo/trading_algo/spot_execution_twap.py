"""
Binance SPOT TWAP algo
"""
import math
import os
import time

import pandas as pd
from logger_client import LoggerClient

from local_credentials.api_key_exchanges import BINANCE_KEY, BINANCE_SECRET
from python.crypto.exchanges.binance.rest.binance_spot import BinanceSpot


class TwapAlgo(BinanceSpot, LoggerClient):
    """
    Args:
        BinanceSpot (_type_): binance spot client
        LoggerClient (_type_): logging client
    """

    def __init__(self, apikey, apisecret, file_path, file_name, save_mode):
        BinanceSpot.__init__(self, apikey, apisecret)
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        # SlackClient.__init__(self, token)

        self.base_ticker = None
        self.quote_ticker = None
        self.binance_symbol = None
        self.direction = None
        self.clip_size_type = None
        self.clip_value_limit = None
        self.total_trade_size = None
        self.total_twap_time_seconds = None
        self.time_interval_seconds = None
        self.client_order_id = None

        self.symbol = None
        self.number_of_clips = None
        self.clip_size = None

        self.ticker_current_price = None
        self.required_balance = None

        self.trading_check_counter = 0

    def get_coin_value(self, symbol: str):
        """
        Args:
            symbol: 'BTC' or 'ETH' etc...

        returns symbol valuation in USDT terms, or 1 if stablecoin
        """

        stablecoin_list = ["USDT", "TUSD", "BUSD"]

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
        exchange_info = self.get_exchange_infomation()
        df_exchange_info = pd.DataFrame(exchange_info["symbols"])
        df_symbol_info = df_exchange_info.loc[df_exchange_info["symbol"] == ticker]

        return df_symbol_info

    def get_spot_balance(self, symbol):
        """
        Args:
            symbol: 'BTC', 'ETH', etc...

        returns spot free balance for symbol
        """
        spot_balance = self.get_user_asset()
        df_assets = pd.DataFrame(spot_balance)
        balance = df_assets.loc[df_assets["asset"] == symbol, "free"]

        if not balance.empty:
            bal = float(balance.values[0])
        else:
            bal = 0

        return bal

    def twap_order_checking(self, order_params: dict):
        """SPOT TWAP order checking
        can be in terms of base or quote currency
        will do a couple of checks before placing orders

        Args:
            order_params: order parameters
        """

        # counter for checks
        self.trading_check_counter = 0

        ### trading parameters ###
        self.base_ticker = order_params["base_ticker"]
        self.quote_ticker = order_params["quote_ticker"]
        self.binance_symbol = order_params["binance_symbol"]
        self.direction = order_params["direction"]
        self.clip_size_type = order_params["clip_size_type"]
        self.clip_value_limit = order_params["clip_value_limit"]
        self.total_trade_size = order_params["total_trade_size"]
        self.total_twap_time_seconds = order_params["total_twap_time_seconds"]
        self.time_interval_seconds = order_params["time_interval_seconds"]
        self.client_order_id = order_params["client_order_id"]

        ##########################

        if self.clip_size_type == "base":
            self.symbol = self.base_ticker
        elif self.clip_size_type == "quote":
            self.symbol = self.quote_ticker

        print(f"{self.binance_symbol} TWAP {self.direction} order")
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
            decimal_place = int(math.log(1 / step_size, 10))
            self.clip_size = round(
                self.total_trade_size / self.number_of_clips, decimal_place
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
        if clip_value < 10:
            print("clip value less than binance min trade size of 10 USD")
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
            self.get_symbol_price_ticker(params={"symbol": self.binance_symbol})[
                "price"
            ]
        )

        if self.direction == "BUY" and self.clip_size_type == "base":
            # check if sufficient quote asset balance
            self.required_balance = self.ticker_current_price * self.total_trade_size
            if quote_asset_balance < self.required_balance:
                print("insufficient quote balance")
                print(f"current quote balance = {quote_asset_balance}")
                print(f"required quote balance = {self.required_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "BUY" and self.clip_size_type == "quote":
            self.required_balance = self.total_trade_size
            if quote_asset_balance < self.required_balance:
                print("insufficient quote balance")
                print(f"current quote balance = {quote_asset_balance}")
                print(f"required quote balance = {self.required_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "base":
            self.required_balance = self.total_trade_size
            if base_asset_balance < self.required_balance:
                print("insufficient base balance")
                print(f"required base balance = {self.required_balance}")
                print(f"current base balance = {base_asset_balance}")
                self.trading_check_counter += 1
                return None

        elif self.direction == "SELL" and self.clip_size_type == "quote":
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
            # either quantity or quoteOrderQty
            clip_size_type = self.clip_size_type

            if clip_size_type == "base":
                placing_order_params["quantity"] = self.clip_size
            elif clip_size_type == "quote":
                placing_order_params["quoteOrderQty"] = self.clip_size

            # placing order in clips
            time_interval_seconds = self.time_interval_seconds
            number_of_clips = self.total_twap_time_seconds / self.time_interval_seconds
            for i in range(int(number_of_clips)):
                order = self.post_new_order(placing_order_params)
                print(order)
                self.logger.info(order)
                order_id = order["orderId"]
                print(order_id)
                print(f"clip {i+1} of {number_of_clips} done")
                print(f"sleeping for {time_interval_seconds} seconds")
                time.sleep(time_interval_seconds)


if __name__ == "__main__":
    # for saving logs
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "twap_execution.log"

    # initializing
    client = TwapAlgo(
        apikey=BINANCE_KEY,
        apisecret=BINANCE_SECRET,
        file_path=save_path,
        file_name=FILENAME,
        save_mode="a",
    )
    # order parameters
    params = {
        "base_ticker": "ETH",  # base ticker
        "quote_ticker": "BTC",  # quote ticker
        "binance_symbol": "ETHBTC",  # full ticker
        "direction": "BUY",  # BUY or SELL
        "clip_size_type": "base",  # 'base' or 'quote' currency
        "total_trade_size": 0.05,  # trade size in clip_size_type
        "clip_value_limit": 5000,  # clip size limit of 5k USD per clip
        "total_twap_time_seconds": 50,  # total time of twap
        "time_interval_seconds": 10,  # execution interval
        "client_order_id": "testing",  # unique order id
    }
    # checking here
    # client.twap_order_checking(params)
    # client.post_message

    # uncomment to place order
    client.place_twap_order(params)
