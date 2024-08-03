"""
pip install sqlalchemy
connecting to sql databases using sqlalchemy
"""

import datetime as dt

import pandas as pd
import sqlalchemy
from local_credentials.db_credentials import SGTRD3_MARKETDATA_WRITE
from local_credentials.email_settings import (
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT_RISK,
    EMAIL_USER,
)
from python.sg1_server.cronjobs.risk_monitoring.proof_of_reserves.send_emails import (
    send_email,
)
from python.sg1_server.cronjobs.risk_monitoring.telegram_client import Telegram
from sqlalchemy import create_engine, inspect


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
            FROM exchange_por
            order by date desc
            limit 10000
            """
        )
        try:
            df_query = pd.read_sql_query(query, self.connection)
            return df_query

        except Exception as error:
            print(f"Error executing query: {error}")

    def por_monitoring(self):
        """
        pulls data from proof of reserves table in postgres
        compares marketcap from 1hour ago and 1day ago
        """
        df_data = self.get_balances()

        latest_time = df_data.values[0][4]
        previous_hour = latest_time + dt.timedelta(hours=-1)
        previous_day = latest_time + dt.timedelta(hours=-24)

        df_data = df_data.sort_values(by=["exchange", "coin"])
        df_data.drop(columns=["index"], inplace=True)

        df_latest_time = df_data.loc[df_data["date"] == latest_time]
        df_prev_hour = df_data.loc[df_data["date"] == previous_hour]
        df_prev_day = df_data.loc[df_data["date"] == previous_day]

        # does a left join
        df_merge_hour = pd.merge(
            df_latest_time,
            df_prev_hour,
            how="left",
            left_on=["exchange", "coin"],
            right_on=["exchange", "coin"],
        )
        df_merge_day = pd.merge(
            df_latest_time,
            df_prev_day,
            how="left",
            left_on=["exchange", "coin"],
            right_on=["exchange", "coin"],
        )

        # renaming columns after left join
        df_merge_hour.rename(
            columns={
                "final_balance_x": "current_balance",
                "date_x": "current_date",
                "price_x": "current_price",
                "market_cap_x": "current_market_cap",
                "final_balance_y": "previous_balance",
                "date_y": "previous_date",
                "price_y": "previous_price",
                "market_cap_y": "previous_market_cap",
            },
            inplace=True,
        )
        df_merge_day.rename(
            columns={
                "final_balance_x": "current_balance",
                "date_x": "current_date",
                "price_x": "current_price",
                "market_cap_x": "current_market_cap",
                "final_balance_y": "previous_balance",
                "date_y": "previous_date",
                "price_y": "previous_price",
                "market_cap_y": "previous_market_cap",
            },
            inplace=True,
        )

        # calculates balance diff and % diff
        df_merge_hour["balance_diff"] = (
            df_merge_hour["current_balance"] - df_merge_hour["previous_balance"]
        )
        df_merge_hour["pct_balance_diff"] = (
            df_merge_hour["balance_diff"] / df_merge_hour["current_balance"]
        ) * 100

        df_merge_day["balance_diff"] = (
            df_merge_day["current_balance"] - df_merge_day["previous_balance"]
        )
        df_merge_day["pct_balance_diff"] = (
            df_merge_day["balance_diff"] / df_merge_day["current_balance"]
        ) * 100

        print(df_merge_day)

        send_email(
            EMAIL_USER,
            EMAIL_PASSWORD,
            EMAIL_RECIPIENT_RISK,
            "Exchanges Reserves Monitoring",
            df_merge_day,
        )


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)

    # sending email
    client.por_monitoring()
    client.close_connection()
