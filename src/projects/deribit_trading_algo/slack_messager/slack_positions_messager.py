"""
deribit websocket connector
"""
import datetime as dt
import time
import pandas as pd

from python.projects.deribit_trading.library_files.redis_client import RedisClient
from python.projects.deribit_trading.library_files.slack_client import SlackClient
from python.projects.deribit_trading.library_files.logger_client import LoggerClient


class SlackPositions(RedisClient, SlackClient, LoggerClient):
    """
    Args:
        RedisClient (_type_): takes in redis client class
        SlackClient (_type_): takes in slack client class
        LoggerClient (_type_): logging client class
    """

    def __init__(self, file_path, file_name, save_mode):
        RedisClient.__init__(self)
        SlackClient.__init__(self)
        LoggerClient.__init__(self, file_path, file_name, save_mode)

    def positions_slack(self, symbol: str):
        """send messages to slack"""

        while True:
            decimal_place = 6
            df_positions = self.get_df(f"DERIBIT_{symbol.upper()}_POSITIONS")

            try:
                df_positions_fut = df_positions.loc[df_positions["kind"] == "future"]
            except KeyError:
                df_positions_fut = pd.DataFrame()

            try:
                df_positions_opt = df_positions.loc[df_positions["kind"] == "option"]
            except KeyError:
                df_positions_opt = pd.DataFrame()

            try:
                index_price = round(df_positions["index_price"].mean(), decimal_place)
            except KeyError:
                index_price = 0

            try:
                net_delta = round(df_positions["delta"].sum(), decimal_place)
            except KeyError:
                net_delta = 0

            try:
                net_delta_fut = round(df_positions_fut["delta"].sum(), decimal_place)
            except KeyError:
                net_delta_fut = 0

            try:
                net_delta_opt = round(df_positions_opt["delta"].sum(), decimal_place)
            except KeyError:
                net_delta_opt = 0

            text = f"{str(dt.datetime.now())}\
                    index_price = {str(index_price)}\
                    {symbol}_net_delta = {str(net_delta)}\
                    {symbol}_fut_delta = {str(net_delta_fut)}\
                    {symbol}_opt_delta = {str(net_delta_opt)}"
            self.post_message(
                channel=f"#deribit_{symbol}_positions",
                text=text,
            )
            print("sleeping...")
            time.sleep(60)
