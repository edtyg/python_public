"""
maker execution algo
"""
import datetime as dt
import logging
import os
import time

from trading_params_eth import (
    SHORT_PUT_STRIKE,
    SHORT_CALL_STRIKE,
    STRIKE_INTERVAL,
)

from python.projects.deribit_trading.library_files.deribit_methods import DeribitMethods
from python.projects.deribit_trading.library_files.keys import API_KEY, API_SECRET_KEY
from python.projects.deribit_trading.library_files.redis_client import RedisClient
from python.projects.deribit_trading.library_files.slack_client import SlackClient

################
### logging ####
full_path = os.path.realpath(__file__)
save_path = os.path.dirname(full_path) + "/"
logging.basicConfig(
    filename=save_path + "trading_algo_maker.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="w",
)
logger = logging.getLogger(__name__)
################


class TraderMaker(DeribitMethods):
    """
    maker execution algo
    """

    def options_hedging_algo_maker(self):
        """
        pulls positional data from redis table
        pulls orderbook data from redis table
        if data is off by set amount of time i.e +- 2 seconds,
        trade algo will not be allowed to place orders

        places maker order during fixing
        keeps delta as close to 0 as possible during fix
        runs once every 5 mins
        """
        # send slack messages periodically
        slack_message_count = 300

        while True:
            self.get_delta_limits(
                SHORT_PUT_STRIKE,
                SHORT_CALL_STRIKE,
                STRIKE_INTERVAL,
            )
            print(f"current {self.currency} perp delta = {self.futures_delta}")
            delta_difference = self.futures_expected_delta - self.futures_delta
            print(f"delta_difference = {delta_difference}")

            if (
                self.placing_order_status is True
                and self.futures_expected_delta == 0
                and self.options_positions is True  # expiry options revert to 0
                and self.futures_positions is True  # expiry options revert to 0
            ):
                self.slack_client.post_message(
                    channel=self.slack_channel_trades_records,
                    text=f"{str(dt.datetime.now())} current_perp_delta = {self.futures_delta}\
                    expected_perp_delta = {self.futures_expected_delta}\
                    delta_difference = {delta_difference}\
                    placing limit order",
                )
                self.close_perp_positions()
                print("closing perp positions")

            elif (
                self.placing_order_status is True
                and self.futures_expected_delta == 0
                and self.options_positions is False  # expiry options revert to 0
                and self.futures_positions is True  # expiry options revert to 0
            ):
                self.slack_client.post_message(
                    channel=self.slack_channel_trades_records,
                    text=f"{str(dt.datetime.now())} current_perp_delta = {self.futures_delta}\
                    expected_perp_delta = {self.futures_expected_delta}\
                    delta_difference = {delta_difference}\
                    placing limit order",
                )
                self.close_perp_positions()
                print("closing perp positions")

            #####################
            ### slack message ###
            #####################
            print(f"slack msg count = {slack_message_count}")
            slack_message_count += 1

            if slack_message_count >= 300:
                self.slack_client.post_message(
                    channel=self.slack_channel_maker_status,
                    text=f"{str(dt.datetime.now())} maker trading algo running.\
                    current_perp_delta = {self.futures_delta} \
                    expected_perp_delta = {self.futures_expected_delta}",
                )
                slack_message_count = 0  # reset count

            print("sleeping")
            time.sleep(1)
            print("\n")


if __name__ == "__main__":
    deribit_trading = TraderMaker(
        API_KEY, API_SECRET_KEY, RedisClient(), SlackClient(), "eth"
    )
    deribit_trading.options_hedging_algo_maker()
