"""
pip install sqlalchemy
connecting to sql databases using sqlalchemy
"""
import datetime as dt

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect

from local_credentials.db_credentials import SGTRD3_MARKETDATA_WRITE
from python.sg1_server.cronjobs.risk_monitoring.telegram_client import Telegram

# self.chatgroup_hts_chatbot = "-987081068"  # hts chatbot with gongye
# self.market_information_test = "-990460215"  # main group for chat notifications


class SqlAlchemyConnector(Telegram):
    """connector for sql databases"""

    def __init__(self, credentials: dict):
        Telegram.__init__(self)
        self.host = credentials["HOST"]
        self.database = credentials["DB"]
        self.user = credentials["USER"]
        self.port = credentials["PORT"]
        self.password = credentials["PASSWORD"]

        self.engine = None
        self.connection = None
        self.connection_type = None
        self.postgres_connection()

    def postgres_connection(self):
        """connecting to a postgresql"""
        self.connection_type = "postgresql"

        try:
            database_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

            self.engine = create_engine(database_url)
            self.connection = self.engine.connect()
            insp = inspect(self.connection)

            print(f"connected to pgsql database = {self.host} with user = {self.user}")
            print(f"tables available = {insp.get_table_names()}")

        except sqlalchemy.exc.OperationalError as error:
            print(error)

    def close_connection(self):
        """closing connection"""

        self.connection.close()
        self.engine.dispose()
        print(f"{self.connection_type} connection closed")

    def get_balances(self):
        """selecting a table"""

        query = sqlalchemy.text(
            """
            SELECT *
            FROM curve_3pool_monitor
            order by index desc
            limit 1
            """
        )
        try:
            df_query = pd.read_sql_query(query, self.connection)
            print(df_query)
            return df_query

        except Exception as error:
            print(f"Error executing query: {error}")

    def curve_3pool_monitoring(
        self,
        threshold_primary: float,
        threshold_secondary: float,
    ):
        """
        pulls data from proof of reserves table in postgres
        compares marketcap from 1hour ago and 1day ago
        """
        tg_client = Telegram()

        df_data = self.get_balances()
        dai_pct = df_data["dai_proportion"].values
        usdc_pct = df_data["usdc_proportion"].values
        usdt_pct = df_data["usdt_proportion"].values

        data_dict = {
            "dai_proportion": dai_pct,
            "usdc_proportion": usdc_pct,
            "usdt_proportion": usdt_pct,
        }
        for key, values in data_dict.items():
            if values >= threshold_secondary:
                text = f"{self.fire_emoji*3} curve_3pool {key} greater than threshold of {threshold_secondary} {self.fire_emoji*3}"
                tg_client.send_message(tg_client.market_information_test, text)
            elif values > threshold_primary:
                text = f"{self.alarm_emoji*3} curve_3pool {key} greater than threshold of {threshold_primary} {self.alarm_emoji*3}"
                tg_client.send_message(tg_client.market_information_test, text)
            else:
                print("within threshold")


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)

    THRESHOLD_PRIMARY = 0.5
    THRESHOLD_SECONDARY = 0.7
    client.curve_3pool_monitoring(THRESHOLD_PRIMARY, THRESHOLD_SECONDARY)
