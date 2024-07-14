"""
pip install sqlalchemy
connecting to sql databases using sqlalchemy
"""

import sqlalchemy.exc
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.url import URL

from keys.api_personal.databases.mysql import MYSQL_WINDOWS_ADMIN
from keys.api_personal.databases.postgres import PGSQL_VM_ADMIN


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
                    drivername="postgresql+psycopg2",
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                )
            elif db_type == "mysql":
                database_url = URL.create(
                    drivername="mysql+mysqlconnector",
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                )
            else:
                raise ValueError("Unsupported database type")

            self.engine = create_engine(database_url)

        except sqlalchemy.exc.OperationalError as error:
            print(f"Error connecting to {db_type} database: {error}")
        except ValueError as error:
            print(error)

    def list_tables(self, db_type: str):
        """list all available tables for this database"""
        self.connect(db_type)

        with self.engine.connect() as conn:
            insp = inspect(conn)
            print(
                f"Connected to {db_type} database at {self.host} with user {self.user}"
            )
            print(f"Tables available: {insp.get_table_names()}")


if __name__ == "__main__":
    # Example usage

    pgconn = "postgres"
    print("Connecting to Postgres client...")
    postgres_client = SqlAlchemyConnector(PGSQL_VM_ADMIN)
    postgres_client.connect(pgconn)
    postgres_client.list_tables(pgconn)
    print("\n")

    mysqlconn = "mysql"
    print("Connecting to MySQL client...")
    mysql_client = SqlAlchemyConnector(MYSQL_WINDOWS_ADMIN)
    mysql_client.connect(mysqlconn)
    mysql_client.list_tables(mysqlconn)
    print("\n")
