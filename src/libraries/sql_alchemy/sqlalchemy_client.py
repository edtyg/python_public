"""
pip install sqlalchemy
SQLAlchemy 2.0.29
connecting to sql databases using sqlalchemy
"""

import sqlalchemy
from sqlalchemy import create_engine, inspect

from keys.api_personal.databases.mysql import MYSQL_UBUNTU_ADMIN
from keys.api_personal.databases.postgres import PGSQL_UBUNTU_ADMIN


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
                database_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            elif db_type == "mysql":
                database_url = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
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
    postgres_client = SqlAlchemyConnector(PGSQL_UBUNTU_ADMIN)
    postgres_client.connect("postgres")
    print("\n")

    print("Connecting to MySQL client...")
    mysql_client = SqlAlchemyConnector(MYSQL_UBUNTU_ADMIN)
    mysql_client.connect("mysql")
    print("\n")
