"""
pip install sqlalchemy
SQLAlchemy 2.0.22
connecting to sql databases using sqlalchemy
"""

import sqlalchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL

from keys.api_work.databases.postgres import SG_TRADING_2_MARKETDATA_WRITE


class SqlAlchemyConnector:
    """A connector for SQL databases."""

    def __init__(self, credentials: dict):
        """
        Initialize the connector.

        Args:
            credentials (dict): A dictionary containing HOST, DB, USER, PORT, PASSWORD.
        """
        self.host = credentials["HOST"]
        self.database = credentials["DB"]
        self.user = credentials["USER"]
        self.port = credentials["PORT"]
        self.password = credentials["PASSWORD"]

        self.engine = None
        self.connection_type = None

    def connect(self, db_type: str):
        """
        Connect to a database.

        Args:
            db_type (str): Type of database ('postgresql' or 'mysql').
        """
        self.connection_type = db_type

        try:
            if db_type == "postgres":
                database_url = URL.create(
                    "postgresql+psycopg2",
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    database=self.database,
                    port=self.port,
                )
            elif db_type == "mysql":
                database_url = URL.create(
                    "mysql+mysqlconnector",
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    database=self.database,
                    port=self.port,
                )
            else:
                raise ValueError("Unsupported database type")

            self.engine = create_engine(database_url)

            with self.engine.connect() as conn:
                insp = inspect(conn)
                print(
                    f"Connected to {db_type} database at {self.host} with user {self.user}"
                )
                print(f"Tables available: {insp.get_table_names()}")

        except sqlalchemy.exc.OperationalError as error:
            print(f"Error connecting to {db_type} database: {error}")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    # Example usage
    print("Connecting to Postgres client...")
    postgres_client = SqlAlchemyConnector(SG_TRADING_2_MARKETDATA_WRITE)
    postgres_client.connect("postgres")
    print("\n")
