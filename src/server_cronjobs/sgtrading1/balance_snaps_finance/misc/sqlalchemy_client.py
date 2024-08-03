"""
pip install sqlalchemy
connecting to sql databases using sqlalchemy
"""

import sqlalchemy
from sqlalchemy import create_engine, inspect, text

from src.server_cronjobs.sgtrading1.balance_snaps_finance.misc.credentials import (
    SGTRD3_MARKETDATA_WRITE,
)


class SqlAlchemyConnector:
    """connector for sql databases"""

    def __init__(self, credentials: dict):
        self.host = credentials["HOST"]
        self.database = credentials["DB"]
        self.user = credentials["USER"]
        self.port = credentials["PORT"]
        self.password = credentials["PASSWORD"]

        self.engine = None
        self.connection = None
        self.connection_type = None

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


if __name__ == "__main__":
    client = SqlAlchemyConnector(SGTRD3_MARKETDATA_WRITE)
    client.postgres_connection()
    # client.close_connection()

    query = "select * from account_balances"
    result = client.connection.execute(text(query))
    print(result.fetchall())
