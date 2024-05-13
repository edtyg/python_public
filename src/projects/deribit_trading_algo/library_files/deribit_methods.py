"""
methods build on top of deribit's api
"""
import datetime as dt
import time

import pandas as pd

from local_credentials.api_key_exchanges import DERIBIT_KEY, DERIBIT_SECRET
from python.projects.deribit_trading_algo.library_files.deribit_rest_client import (
    DeribitRestClient,
)
from python.projects.deribit_trading_algo.library_files.redis_client import RedisClient
from python.projects.deribit_trading_algo.library_files.slack_client import SlackClient


class DeribitMethods(DeribitRestClient):
    """
    A class that extends the DeribitRestClient class and provides additional
    methods for managing Deribit API operations.

    Args:
        apikey (str): API key for Deribit API authentication.
        apisecret (str): API secret for Deribit API authentication.
        redis_client: Redis client for interacting with Redis database.
        slack_client: Slack client for sending messages to Slack channels.
        currency (str): Currency for which the operations are performed.

    Attributes:
        currency (str): Currency for which the operations are performed.
        perp_instrument (str): Perpetual instrument name.
        redis_client: Redis client for interacting with Redis database.
        slack_client: Slack client for sending messages to Slack channels.
        slack_channel_maker_status (str): Slack channel name for maker algorithm status.
        slack_channel_taker_status (str): Slack channel name for taker algorithm status.
        slack_channel_trades_records (str): Slack channel name for trade executions.
        slack_channel_positions (str): Slack channel name for positions.
        options_positions: bool: Flag indicating if there are any options positions
        futures_positions: bool: Flag indicating if there are any futures positions
        options_delta (float): Sum of delta values for all options positions.
        futures_delta (float): Sum of delta values for all futures positions.
        net_delta (float): Sum of options and futures delta values.
        call_option_pos (int): Total size of call options positions.
        put_option_pos (int): Total size of put options positions.
        perp_pos (float): Total size of perpetual futures positions in USD.
        placing_order_status (bool): Flag indicating if orders can be placed
        bid (float): Top of orderbook bid price.
        ask (float): Top of orderbook ask price.
        index_price (float): Current index price.
        time_diff_lower_limit (int): Lower limit for time difference
        time_diff_upper_limit (int): Upper limit for time difference
    """

    def __init__(
        self, apikey: str, apisecret: str, redis_client, slack_client, currency: str
    ):
        super().__init__(apikey, apisecret)

        # currency
        self.currency = currency
        self.perp_instrument = f"{self.currency.upper()}-PERPETUAL"

        # redis database
        self.redis_client = redis_client

        # slack client and channels
        self.slack_client = slack_client

        self.slack_channel_maker_status = (
            f"#deribit_{currency}_algo_maker_status"  # maker algo status channel
        )
        self.slack_channel_taker_status = (
            f"#deribit_{currency}_algo_taker_status"  # taker algo status channel
        )

        self.slack_channel_trades_records = (
            f"#deribit_{currency}_algo_trades"  # trade executions channel
        )
        self.slack_channel_positions = (
            f"#deribit_{currency}_positions"  # trade executions channel
        )

        # check if there are any options or futures positions running
        self.options_positions = None
        self.futures_positions = None

        # options and futures delta
        self.options_delta = None
        self.futures_delta = None
        self.net_delta = None  # net_delta = sum of both options and futures delta

        # options positions in coin terms
        self.call_option_pos = None
        self.put_option_pos = None

        # perpetual futures positions in USD
        self.perp_pos = None

        # placing orders status
        self.placing_order_status = None

        # top of orderbook prices
        self.bid = None
        self.ask = None

        # index_price
        self.index_price = None

        # expected perp delta
        self.futures_expected_delta = None

        # redis - positions and orderbook time difference allowance
        self.time_diff_lower_limit = -5
        self.time_diff_upper_limit = 5

    def get_index(self):
        """
        gets current index price from redis
        """
        df_index = self.redis_client.get_df(
            f"DERIBIT_{self.currency.upper()}_USD_INDEX"
        )
        self.index_price = df_index["index_price"].values[0]
        print(f"{self.currency} index price = {self.index_price}")

        # timing check for positions
        if not df_index.empty:
            time_frm_df = df_index.index[0].timestamp()
            curr_time = dt.datetime.now().timestamp()
            time_diff = curr_time - time_frm_df

            # order placing status check
            if self.time_diff_lower_limit <= time_diff <= self.time_diff_upper_limit:
                self.placing_order_status = True
                print("positions within time limits; placing order status = True")
            else:
                self.placing_order_status = False
                print("positions not within time limits; placing order status = False")

            print(f"time difference = {time_diff}")

    def get_current_pos(self):
        """
        pulls positional data from redis tables
        if data is off by set amount of time i.e +- 2 seconds,
        trade algo will not be allowed to place orders
        """
        # pulls positions from redis
        df_redis = self.redis_client.get_df(
            f"DERIBIT_{self.currency.upper()}_POSITIONS"
        )

        # filters by options or futures
        try:
            df_options = df_redis.loc[df_redis["kind"] == "option"]
        except KeyError:
            df_options = pd.DataFrame()

        try:
            df_futures = df_redis.loc[df_redis["kind"] == "future"]
        except KeyError:
            df_futures = pd.DataFrame()

        try:
            if df_futures["size"].sum() == 0:
                df_futures = pd.DataFrame()
        except KeyError:
            df_futures = pd.DataFrame()

        # options pos and delta
        if not df_options.empty:
            self.options_positions = True
            self.call_option_pos = df_options.loc[
                df_options["instrument_name"].str.endswith("C"), "size"
            ].sum()
            self.put_option_pos = df_options.loc[
                df_options["instrument_name"].str.endswith("P"), "size"
            ].sum()
            print(f"{self.currency} options positions = true")
            print(f"{self.currency} call options size = {self.call_option_pos}")
            print(f"{self.currency} put options size = {self.put_option_pos}")

            self.options_delta = round(df_options["delta"].sum(), 4)
            print(f"{self.currency} options delta = {self.options_delta}")

        else:
            self.options_positions = False
            self.call_option_pos = 0
            self.put_option_pos = 0
            print(f"{self.currency} options positions = false")

            self.options_delta = 0
            print(f"{self.currency} options delta = 0")

        # futures pos, delta and usd pos size
        if not df_futures.empty:
            self.futures_positions = True
            print(f"{self.currency} futures positions = true")

            self.futures_delta = round(df_futures["delta"].sum(), 4)
            print(f"{self.currency} futures delta = {self.futures_delta}")

            self.perp_pos = df_futures["size"].sum()
            print(f"{self.currency} perpetual futures size in usd = {self.perp_pos}")
        else:
            self.futures_positions = False
            print(f"{self.currency} futures positions = false")

            self.futures_delta = 0
            print(f"{self.currency} futures delta = 0")

            self.perp_pos = 0
            print(f"{self.currency} perpetual futures size in usd = 0")

        self.net_delta = self.options_delta + self.futures_delta
        print(f"{self.currency} net delta = {self.net_delta}")

        # timing check for positions
        if not df_redis.empty:
            time_frm_df = df_redis.index[0].timestamp()
            curr_time = dt.datetime.now().timestamp()
            time_diff = curr_time - time_frm_df

            # order placing status check
            if self.time_diff_lower_limit <= time_diff <= self.time_diff_upper_limit:
                self.placing_order_status = True
                print("positions within time limits; placing order status = True")
            else:
                self.placing_order_status = False
                print("positions not within time limits; placing order status = False")
            print(f"time difference = {time_diff}")
        else:
            print("empty df")

    def get_perps_orderbook_price(self):
        """
        pulls top of orderbook data
        if data is off by set amount of time i.e +- 2 seconds,
        trade algo will not be allowed to place orders
        """
        # pulls positions from redis
        df_orderbook = self.redis_client.get_df(
            f"DERIBIT_{self.currency.upper()}-PERPETUAL_ORDERBOOK"
        )

        if not df_orderbook.empty:
            time_frm_df = df_orderbook.index[0].timestamp()
            curr_time = dt.datetime.now().timestamp()
            time_diff = curr_time - time_frm_df

            self.bid = df_orderbook["bid"][0]
            print(f"{self.currency} highest bid = {self.bid}")

            self.ask = df_orderbook["ask"][0]
            print(f"{self.currency} lowest ask = {self.ask}")

            # order placing status check
            if self.time_diff_lower_limit <= time_diff <= self.time_diff_upper_limit:
                self.placing_order_status = True
                print("orderbook snaps within time limits; placing order status = True")
            else:
                self.placing_order_status = False
                print(
                    "orderbook snaps not within time limits; placing order status = False"
                )

            print(f"time difference = {time_diff}")

    def place_perps_maker_order(self, size: float, direction: str, reduce_only: str):
        """
        size = usd amount; take note of contract size 10 for btc, 1 for eth
        direction = 'buy' or 'sell'
        reduce only = 'true' or 'false'
        """
        order_placed = False
        order_filled = False

        #############################
        ### placing initial order ###
        #############################

        if direction == "buy":
            self.get_perps_orderbook_price()
            if self.placing_order_status is True:
                order = self.place_buy_order(
                    params={
                        "instrument_name": self.perp_instrument,
                        "price": self.bid,
                        "amount": size,
                        "type": "limit",
                        "time_in_force": "good_til_cancelled",
                        "post_only": "true",
                        "reduce_only": reduce_only,
                    }
                )
                print("placing maker buy order")
                # print(order)

        elif direction == "sell":
            self.get_perps_orderbook_price()
            if self.placing_order_status is True:
                order = self.place_sell_order(
                    params={
                        "instrument_name": self.perp_instrument,
                        "price": self.ask,
                        "amount": size,
                        "type": "limit",
                        "time_in_force": "good_til_cancelled",
                        "post_only": "true",
                        "reduce_only": reduce_only,
                    }
                )
                print("placing maker sell order")
                # print(order)

        try:
            result = order["result"]  # if order placed through there will be a result
            order_placed = True
            print(result)

        except KeyError:
            result = None  # order not placed - either timing off or other reasons
            order_placed = False
            print(order["error"])
            return order["error"]

        # initial order placed
        if order_placed is True:
            order_id = result["order"]["order_id"]
            print(f"order_id = {order_id}")
        time.sleep(0.5)

        # check if order is filled
        # if not filled - updates price to top of orderbook
        while order_filled is False:
            order_status = self.get_order_state(params={"order_id": order_id})
            order_amount = order_status["result"]["amount"]
            filled_amount = order_status["result"]["filled_amount"]
            remaining_amount = order_amount - filled_amount
            order_filled_status = order_status["result"]["order_state"]

            print(f"filled_amount = {filled_amount}")
            print(f"remaining_amount = {remaining_amount}")

            if order_filled_status == "filled":
                order_filled = True  # exits loop
                print("order fully filled")
            else:
                self.get_perps_orderbook_price()
                if direction == "buy":
                    order = self.edit_order(
                        params={
                            "order_id": order_id,
                            "price": self.bid,
                            "amount": remaining_amount,
                        }
                    )
                elif direction == "sell":
                    order = self.edit_order(
                        params={
                            "order_id": order_id,
                            "price": self.ask,
                            "amount": remaining_amount,
                        }
                    )
            time.sleep(0.5)
        return None

    def close_perp_positions(self):
        """does a maker order to close all existing perp futures positions"""
        self.get_current_pos()
        position = self.perp_pos
        order_size = abs(position)

        if position < 0:
            self.place_perps_maker_order(order_size, "buy", "false")
        elif position > 0:
            self.place_perps_maker_order(order_size, "sell", "false")

    def get_delta_limits(
        self,
        short_put_strike: float,
        short_call_strike: float,
        strike_interval: float,
    ):
        """
        uses strike price of short call and short put
        sets an interval at these strike prices
        e.g.
        short put at 30000 -> sets interval of 500 -> [29500, 30500]
        short call at 32000 -> sets interval of 500 -> [31500, 32500]

        """
        self.get_current_pos()
        self.get_index()

        # index nearing short call region
        short_call_strike_lower = short_call_strike - strike_interval
        short_call_strike_upper = short_call_strike + strike_interval
        self.call_option_interval = [short_call_strike_lower, short_call_strike_upper]
        print(
            f"call option interval = [{short_call_strike_lower},{short_call_strike_upper}]"
        )

        # index nearing short put region
        short_put_strike_lower = short_put_strike - strike_interval
        short_put_strike_upper = short_put_strike + strike_interval
        self.put_option_interval = [short_put_strike_lower, short_put_strike_upper]
        print(
            f"put option interval = [{short_put_strike_lower},{short_put_strike_upper}]"
        )

        if short_call_strike_lower <= self.index_price <= short_call_strike_upper:
            futures_expected_delta = (
                (self.index_price - short_call_strike_lower) / (2 * strike_interval)
            ) * abs(self.call_option_pos)
        elif short_put_strike_upper < self.index_price < short_call_strike_lower:
            futures_expected_delta = 0
        elif self.index_price > short_call_strike_upper:
            futures_expected_delta = abs(self.call_option_pos)

        if short_put_strike_lower <= self.index_price <= short_put_strike_upper:
            futures_expected_delta = (
                (short_put_strike_upper - self.index_price) / (2 * strike_interval)
            ) * self.put_option_pos
        elif self.index_price < short_put_strike_lower:
            futures_expected_delta = self.put_option_pos
        elif short_put_strike_upper < self.index_price < short_call_strike_lower:
            futures_expected_delta = 0

        self.futures_expected_delta = round(futures_expected_delta, 4)
        print(f"expected perp delta = {self.futures_expected_delta}")


if __name__ == "__main__":
    deribit_client_btc = DeribitMethods(
        DERIBIT_KEY, DERIBIT_SECRET, RedisClient(), SlackClient(), "btc"
    )
    deribit_client_eth = DeribitMethods(
        DERIBIT_KEY, DERIBIT_SECRET, RedisClient(), SlackClient(), "eth"
    )
    # deribit_client_btc.get_current_pos()
    # print("\n")
    # deribit_client_eth.get_current_pos()
    # print("\n")

    # deribit_client_btc.get_perps_orderbook_price()
    # print("\n")
    # deribit_client_eth.get_perps_orderbook_price()
    # print("\n")

    # deribit_client_btc.get_index()
    # print("\n")
    # deribit_client_eth.get_index()
    # print("\n")

    # place maker order
    # deribit_client_btc.place_perps_maker_order(10, 'sell', 'false')
    # deribit_client_eth.place_perps_maker_order(1, 'sell', 'false')

    # close perps
    # deribit_client_btc.close_perp_positions()
    # deribit_client_eth.close_perp_positions()

    # delta_limits_btc = deribit_client_btc.get_delta_limits(29000, 31000, 500)
    # delta_limits_eth = deribit_client_eth.get_delta_limits(1800, 1900, 25)
