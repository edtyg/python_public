"""
taker execution algo
"""
import datetime as dt
import logging
import os
import time

from trading_params_eth import (
    CONTRACT_SIZE,
    SHORT_PUT_STRIKE,
    SHORT_CALL_STRIKE,
    STRIKE_INTERVAL,
    DELTA_THRESHOLD,
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
    filename=save_path + "trading_algo_taker.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filemode="w",
)
logger = logging.getLogger(__name__)
################


class TraderTaker(DeribitMethods):
    """
    taker execution algo
    """

    def options_hedging_algo_taker(self):
        """
        pulls expected delta based on position size and interval setting
        if data is off by set amount of time i.e +- 2 seconds,
        trade algo will not be allowed to place orders
        runs every second but will only post messages to slack once every minute
        """
        # send slack messages periodically
        slack_message_count = 60

        while True:
            self.get_delta_limits(
                SHORT_PUT_STRIKE,
                SHORT_CALL_STRIKE,
                STRIKE_INTERVAL,
            )
            logging.info(f'call strike interval = {self.call_option_interval}')
            logging.info(f'put strike interval = {self.put_option_interval}')
            print(f"current {self.currency} perp delta = {self.futures_delta}")
            delta_difference = self.futures_expected_delta - self.futures_delta
            print(f"delta_difference = {delta_difference}")

            if (
                self.placing_order_status is True
                and delta_difference > 0
                and abs(delta_difference) >= DELTA_THRESHOLD
                and self.options_positions is True  # expiry options revert to 0
            ):
                self.slack_client.post_message(
                    channel=self.slack_channel_trades_records,
                    text=f"{str(dt.datetime.now())} current_perp_delta = {self.futures_delta}\
                    expected_perp_delta = {self.futures_expected_delta}\
                    delta_difference = {delta_difference}\
                    placing market buy order",
                )
                # replace taker orders with maker orders
                
                # order = self.place_buy_order(
                #     params={
                #         "instrument_name": self.perp_instrument,
                #         "amount": round(
                #             (self.index_price * abs(delta_difference)) / CONTRACT_SIZE
                #         )
                #         * CONTRACT_SIZE,
                #         "type": "market",
                #     }
                # )
                order = self.place_perps_maker_order(
                    size = round(
                        (self.index_price * abs(delta_difference)) / CONTRACT_SIZE
                    )
                    * CONTRACT_SIZE,
                    direction = 'buy',
                    reduce_only = 'false',
                    )
                logger.info(order)
                print("buy order placed")

            elif (
                self.placing_order_status is True
                and delta_difference < 0
                and abs(delta_difference) >= DELTA_THRESHOLD
                and self.options_positions is True  # expiry options revert to 0
            ):
                self.slack_client.post_message(
                    channel=self.slack_channel_trades_records,
                    text=f"{str(dt.datetime.now())} current_perp_delta = {self.futures_delta}\
                    expected_perp_delta = {self.futures_expected_delta}\
                    delta_difference = {delta_difference}\
                    placing market sell order",
                )
                # replace taker orders with maker orders
                
                # order = self.place_sell_order(
                #     params={
                #         "instrument_name": self.perp_instrument,
                #         "amount": round(
                #             (self.index_price * abs(delta_difference)) / CONTRACT_SIZE
                #         )
                #         * CONTRACT_SIZE,
                #         "type": "market",
                #     }
                # )
                order = self.place_perps_maker_order(
                    size = round(
                        (self.index_price * abs(delta_difference)) / CONTRACT_SIZE
                    )
                    * CONTRACT_SIZE,
                    direction = 'sell',
                    reduce_only = 'false',
                    )
                logger.info(order)
                print("sell order placed")

            #####################
            ### slack message ###
            #####################
            print(f"slack msg count = {slack_message_count}")
            slack_message_count += 1

            if slack_message_count >= 60:
                self.slack_client.post_message(
                    channel=self.slack_channel_taker_status,
                    text=f"{str(dt.datetime.now())} taker trading algo running.\
                    current_perp_delta = {self.futures_delta} \
                    expected_perp_delta = {self.futures_expected_delta}\
                    hedging_threshold = {DELTA_THRESHOLD}",
                )
                slack_message_count = 0  # reset count

            print("sleeping")
            time.sleep(1)
            print("\n")


if __name__ == "__main__":
    deribit_trading = TraderTaker(
        API_KEY, API_SECRET_KEY, RedisClient(), SlackClient(), "eth"
    )
    deribit_trading.options_hedging_algo_taker()
